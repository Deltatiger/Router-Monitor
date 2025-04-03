import json

class UsageStats:
    """
    Usage Status Model that is persisted on disk
    """
    
    def __init__(self, json_data: str):
        """
        Constructor
        """
        self.last_read_time = ''
        self.last_read_value = {}
        self.accumulated_value = {}
        
        if json_data is not None and len(json_data) > 0:
            self.load_from_json_str(json_data)
        
    def __str__(self) -> str:
        """
        Converts the object to JSON Data
        """
        json_data = {}
        json_data['last_read_time'] = self.last_read_time
        json_data['last_read_value'] = self.last_read_value
        json_data['accumulated_value'] = self.accumulated_value
        return json.dumps(json_data)
    
    def load_from_json_str(self, data: str) -> None:
        """
        Load the data from the JSON String
        """
        object_data = json.loads(data)
        self.last_read_time = object_data['last_read_time']
        self.last_read_value = object_data['last_read_value']
        self.accumulated_value = object_data['accumulated_value']