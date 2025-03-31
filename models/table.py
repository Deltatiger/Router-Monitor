from utils.string import ljust

class Table:
    """
    Model that represents a generic table with a heading
    """
    def __init__(self, headers: list[str], rows: list[list]):
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
        row_data = {}
        for header_index in range(0, len(self._headers)):
            row_data[self._headers[header_index]] = self._rows[index][header_index]
        return row_data
    
    def get_cell(self, row_index: int, column: str):
        """
        Gets the value of the cell represented by the Column and Row
        """
        header_index = self._headers.index(column)
        return self._rows[row_index][header_index]
    
    def __len__(self) -> int:
        """
        Gets the number of rows for the table
        """
        return len(self._rows)
    
    def __str__(self) -> str:
        """
        Returns the representation of the table
        """
        col_widths = [max(len(str(item)) for item in col) for col in zip(*([self._headers] + self._rows))]
        printable = ''
        
        # Header Row
        printable += " | ".join(ljust(str(item), width) for item, width in zip(self._headers, col_widths))
        printable += "\n"
        # Body Row
        for row in self._rows:
            printable += " | ".join(ljust(str(item), width) for item, width in zip(row, col_widths))
            printable += "\n"
        
        return printable