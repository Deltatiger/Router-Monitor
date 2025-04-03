from models.usage_stats import UsageStats

class UsageTracker:
    """
    Class used for Usage Tracking of the Router Usage
    """
    
    def __init__(self, stats_file_path: str):
        """
        Constructor
        """
        self._stats_file_path = stats_file_path
        self._usage_stats_data: UsageStats = None
        
    def initialize(self) -> None:
        """
        Initialize the Usage data from disk
        """
        # Check if the file exists and load from it.
        json_data = ''
        try:
            fp = open(self._stats_file_path, 'r')
            json_data = ''.join(fp.readlines())
        except:
            json_data = ''
        self._usage_stats_data = UsageStats(json_data)
        
    def set_random_stats(self) -> None:
        """
        Sets random data for the values
        """
        self._usage_stats_data.last_read_value = { "ap1": 100, "ap2": 200 }
        self._usage_stats_data.last_read_time = 150
        
    def persists_stats_to_disk(self) -> bool:
        """
        Persists the Usage Stats Data on Disk
        """
        json_data = str(self)
        try:
            fp = open(self._stats_file_path, 'w')
            fp.write(json_data)
        except:
            return False
        return True
    def __str__(self) -> str:
        """
        Prints the Representation of the Objecet
        """
        return self._usage_stats_data.__str__()