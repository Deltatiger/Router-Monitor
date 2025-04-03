import urequests as requests
from utils.html import extract_table, extract_generic_html_tag
from models.table import Table
from utils.string import strip_newlines
from models.device import Device

class JioRouterConnector():
    """
    Connetion Manager to the Jio Router
    """

    """
    Resource for the Stats Page
    """
    PLATFORMS_PAGE = 'platform.cgi'
    """
    Device Statistics Page Name
    """
    DEVICE_STATS_PAGE_NAME = 'deviceStatistics.html'
    """
    Page showing the details about the LAN Clients connected to the router
    """
    LAN_CLIENTS_PAGE_NAME = 'lanDhcpLeasedClients.html'
    """
    Page showing the details about the Wireless clients connected to the router
    """
    WLAN_CLIENTS_PAGE_NAME = 'wirelessClients.html'
    """
    Page showing the details of the Device Status
    """
    DEVICE_STATUS_PAGE_NAME = 'deviceStatus.html'

    
    def __init__(self, username: str, password: str, router_base: str, router_ip: str):
        """
        Constructor
        """
        self._username = username
        self._password = password
        self._router_base = router_base
        self._router_ip = router_ip
        self._auth_cookie = ''
    
    def connect(self) -> bool:
        """
        Connects to the Jio Server
        """
        login_headers = self._get_headers()
        login_payload = self._get_login_payload()
        login_payload_serialized = JioRouterConnector._construct_form_body(login_payload)
        login_resource_url = f"http://{self._router_ip}/{self.PLATFORMS_PAGE}"
        login_response = requests.post(
            login_resource_url,
            data=login_payload_serialized,
            headers=login_headers,
            parse_headers=True
        )
        if login_response.status_code == 404:
            print ("Login failed with Error 404")
            return False
        # Extract the required information from the Response
        self._extract_session_cookie(login_response)
        return True
    
    def get_uptime(self) -> int:
        """
        Gets the uptime of the router
        """
        response = self._get_response_for_page(self.DEVICE_STATUS_PAGE_NAME)
        # We only need one string from the Page response
        uptime_tag_contents = extract_generic_html_tag(
            strip_newlines(response.text),
            '<div class="configRow"><label>Uptime</label><p>(.*?)</p></div>'
        )
        print(uptime_tag_contents)
        return 0
        
    def get_usage_statistics(self) -> Table:
        """
        Gets the Usage Statistics from the Router Login Page
        """
        response = self._get_response_for_page(self.DEVICE_STATS_PAGE_NAME)
        table_data = extract_table(strip_newlines(response.text), 'recordsData2')
        return table_data
    
    def get_lan_clients(self) -> list[Device]:
        """
        Gets the LAN clients connected to the router
        """
        response = self._get_response_for_page(self.LAN_CLIENTS_PAGE_NAME)
        table_data = extract_table(strip_newlines(response.text), 'recordsData')
        # Convert the table to list of devices
        devices = []
        for row_iter in range(0, len(table_data)):
            device_data = Device()
            device_data.device_ip = table_data.get_cell(row_iter, 'IPv4 Address')
            device_data.mac_address = table_data.get_cell(row_iter, 'MAC Address')
            device_data.connection_mode = 'LAN'
            devices.append(device_data)
        return devices
    
    def get_wlan_clients(self) -> list[Device]:
        """
        Gets the WLAN Clients connected to the Router
        """
        response = self._get_response_for_page(self.WLAN_CLIENTS_PAGE_NAME)
        table_data = extract_table(strip_newlines(response.text), 'recordsData')
        devices = []
        for row_iter in range(0, len(table_data)):
            device_data = Device()
            device_data.mac_address = table_data.get_cell(row_iter, 'MAC Address')
            device_data.connection_mode = 'WLAN'
            devices.append(device_data)
        return devices
    
    def get_all_clients(self) -> list[Device]:
        """
        Gets all the clients connected to the Router
        """
        wlan_devices = self.get_wlan_clients()
        lan_devices = self.get_lan_clients()
        return wlan_devices + lan_devices

    def close_connnection(self):
        """
        Close the connection and destory the resources
        """
        pass
    
    def _get_login_payload(self) -> dict:
        """
        Creates the Payload required for the Login Process
        """
        return {
            'thispage': 'index.html',
            'button.login.userese.dashboard': 'Login',
            'users.username' : self._username,
            'users.password' : self._password
        }
        
    def _get_headers(self) -> dict:
        """
        Creates the Headers required for the Login Process
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self._router_base,
            "Connection": "keep-alive",
            "Referer": self._router_base + "/platform.cgi",
            "Upgrade-Insecure-Requests": "1"
        }
        if self._auth_cookie is not None:
            headers['cookie'] = self._auth_cookie
        return headers
    
    def _extract_session_cookie(self, response: requests.Response) -> None:
        """
        Extract the required cookie information from the Response
        """
        self._auth_cookie = response.headers['Set-Cookie']
        
    def _get_response_for_page(self, page_name: str) -> requests.Response:
        """
        Makes a GET Response for the page specified
        """
        query_params = dict()
        query_params['page'] = page_name
        query_params_string = JioRouterConnector._construct_form_body(query_params)
        request_url = f"http://{self._router_ip}/{self.PLATFORMS_PAGE}?{query_params_string}"
        headers = self._get_headers()
        response = requests.get(
            request_url,
            headers=headers
        )
        return response
    
    def _dump_page_to_file(self, page_response_text: str) -> None:
        """
        Dump the contents of the response to file
        """
        fp = open('output.out', 'w')
        fp.write(page_response_text)
        fp.close()

    def _construct_form_body(data: dict) -> str:
        """
        Construct a form body response from the given data
        """
        body_data = ''
        for key in data:
            value = data[key]
            body_data = f'{body_data}{key}={value}&'
        # Remove the trailing &
        return body_data[0:-1]