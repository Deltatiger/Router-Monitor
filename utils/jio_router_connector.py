import re
import urequests as requests

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
    Resource for the Users Page
    """
    USERS_PAGE = ''

    
    def __init__(self, username: str, password: str, router_base: str):
        """
        Constructor
        """
        self._username = username
        self._password = password
        self._router_base = router_base
        self._auth_cookie = ''
    
    def connect(self) -> bool:
        """
        Connects to the Jio Server
        """
        login_headers = self._get_headers()
        login_payload = self._get_login_payload()
        login_payload_serialized = JioRouterConnector._construct_form_body(login_payload)
        login_response = requests.post(
            f"{self.ROUTER_BASE}{self.PLATFORMS_PAGE}",
            data=login_payload_serialized,
            headers=login_headers,
            parse_headers=True
        )
        print(login_response.status_code)
        print(login_response.headers)
        if login_response.status_code == 404:
            print ("Login failed with Error 404")
            return False
        # Extract the required information from the Response
        self._extract_session_cookie(login_response)
        return True
    
    def get_usage_statistics(self) -> None:
        """
        Gets the Usage Statistics from the Router Login Page
        """
        response = self._get_usage_page_response()
        print(response.text)
        # Extract the required information from the response as a text.

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

    def _get_usage_page_response(self) -> requests.Response:
        """
        Gets the Response from the Usage Page Request
        """
        query_params = dict()
        query_params['page'] = self.DEVICE_STATS_PAGE_NAME
        query_params_string = JioRouterConnector._construct_form_body(query_params)
        request_url = f"{self._router_base}{self.PLATFORMS_PAGE}?{query_params_string}"
        headers = self._get_headers()
        response = requests.get(
            request_url,
            headers=headers
        )
        return response
    
    def _extract_session_cookie(self, response: requests.Response) -> None:
        """
        Extract the required cookie information from the Response
        """
        self._auth_cookie = response.headers['Set-Cookie']

    def _extract_stats_from_page(self, response: str) -> None:
        """
        Extract Stats from the Page Response Text
        """
        table_start_index = response.index('id="recordsData2"') # This is the second table starting point

        pass
    
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