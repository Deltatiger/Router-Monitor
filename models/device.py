class Device:
    """
    Represents a device connected to the Router
    """
    
    def __init__(self):
        """
        Constructor
        """
        self.device_ip = None
        self.mac_address = None
        self.connected_since = None
        self.connection_mode = None
        
    def __str__(self):
        """
        Gets the string representation of the Device
        """
        return f'IP : {self.device_ip} (MAC : {self.mac_address}) connected for : {self.connected_since} seconds using {self.connection_mode}'