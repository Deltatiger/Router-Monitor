import network
from time import sleep

def _mac_to_str(mac) -> str:
    return ':'.join([f"{b:02X}" for b in mac])

def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print(_mac_to_str(wlan.config('mac')))
    connection_check_iter = 0
    while not wlan.isconnected():
        print (f'Waiting for connection for the {connection_check_iter * 2} second')
        connection_check_iter += 1
        sleep(2)
        if connection_check_iter >= 10:
            return False
    global network_ip
    network_ip = wlan.ifconfig()[0]
    print(network_ip)
    print('Connection established')
    return True