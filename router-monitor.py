import sys
from utils.jio_router_connector import JioRouterConnector
from utils.wlan import connect
from utils.config import read_configuration
from utils.html import extract_table


if __name__ == '__main__':
    data_fp = open('data/sample_data.html')
    full_html_page = ''.join(line.strip() for line in data_fp.readlines())
    table_data = extract_table(full_html_page, 'recordsData2')
    print(table_data)

if __name__ == '__main__1':
    # Read the Configuration
    config = read_configuration('data/config.json')
    
    # Connect to the WLAN
    connection_status = connect(
        config['wlan_ssid'],
        config['wlan_password']
    )
    if not connection_status:
        print('Cannot connect to the WLAN. Aborting.')
        sys.exit(-2)
    
    # Login to the Router Page
    router_connector = JioRouterConnector(
        config['router_username'],
        config['router_password'],
        config['router_base']
    )
    if not router_connector.connect():
        print('Cannot login to the Router. Aborting.')
        sys.exit(-3)
        
    # Read the Device Statistics
    stats = router_connector.get_usage_statistics()
