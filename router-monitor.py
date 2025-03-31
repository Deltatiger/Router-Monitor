import sys
from utils.jio_router_connector import JioRouterConnector
from utils.wlan import connect
from utils.config import read_configuration


if __name__ == '__main__':
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
        config['router_base'],
        config['router_ip']
    )
    if not router_connector.connect():
        print('Cannot login to the Router. Aborting.')
        sys.exit(-3)
    # Get the list of approved MACs
    allowed_macs = set([mac_address.lower() for mac_address in config['known_macs']])
    print(allowed_macs)
    devices = router_connector.get_all_clients()
    for device in devices:
        safe_mac_address = device.mac_address.lower()
        if safe_mac_address not in allowed_macs:
            print(device)
            print('Device is not recognized')