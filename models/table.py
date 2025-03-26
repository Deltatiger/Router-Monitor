class Table:
    """
    Model that represents a generic table with a heading
    """
    def __init__(self, headers: list[str], rows: list[dict]):
        """
        Constructor
        """
        self._headers = headers
        self._rows = rows
        
    def get_headers(self) -> list[str]:
        """
        Gets the headers for the Table
        """
        return self._headers
    
    def get_row(self, index: int) -> dict:
        """
        Gets the row at the given Index
        """
        return self._rows[index]
    
    def get_cell(self, column: str, row_index: number):
        """
        Gets the value of the cell represented by the Column and Row
        """
        return self._rows[row_index][column]