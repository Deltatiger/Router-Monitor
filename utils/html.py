import re
from models.table import Table
# This is the Utils related to the HTML

def extract_table(html_text: str, table_id: str) -> list[dict]:
    """
    Extract the Table information from the HTML DOM and return it in a structured manner
    """
    pattern = re.compile('<table.*?id="' + table_id + '">(.*?)</table>')
    matches = pattern.search(html_text)
    matched_groups = matches.groups()
    
    # Check if we have something.
    if len(matched_groups) == 0:
        # No Group. We are going to abort
        return None
    
    if len(matched_groups) > 1:
        # We matched more tables. Not good. Abort
        return None
    matched_table_data = matched_groups[0]
    
    # Parse the header from the table
    headers = _parse_headings_from_thead(matched_table_data)
    # Parse the body from the table
    table_rows = _parse_table_rows(matched_table_data, headers)
    
    return Table(headers, table_rows)

def _parse_headings_from_thead(table_data: str) -> list[str]:
    """
    Parse the headings labels from the <thead> entries
    Assumption is that we have some <th> inside the <thead><tr></tr></thead> wrappers
    """
    header_content = re.compile('<thead><tr>(.*?)</tr></thead>')
    matches = header_content.search(table_data)
    matched_groups = matches.groups()
    if len(matched_groups) == 0:
        # We don't have any headers. Should be constructed from the tbody directly
        return []
    # Resultant Storage
    headers = []
    # From this, we have to parse the <th>*</th> items
    header_row_content = matched_groups[0]
    th_content_pattern = re.compile('<th>(.*?)</th>')
    while True:
        matches = th_content_pattern.search(header_row_content)
        if not matches or len(matches.groups()) == 0:
            break
        # We found a match. Extract and store it.
        matched_cell = matches.groups()[0]
        headers.append(_strip_html_tags(matched_cell))
        # This only matches the first time, so we have to redo this till we don't find anything else.
        header_row_content = th_content_pattern.sub('', header_row_content, 1)

    return headers


def _parse_table_rows(table_data: str, headers: list[str]) -> list[dict]:
    """
    Parse the full table based on the given headers
    """
    # For some good reason, we have the actual data rows starting with the a class. We can use that for now.
    rows = []
    # Find a row in the text
    row_pattern = re.compile('<tr class="gradeA">(.*?)</tr>')
    while True:
        matches = row_pattern.search(table_data)
        if not matches or len(matches.groups()) == 0:
            break
        matched_row_content = matches.groups()[0]
        # Extract the Columns from the row and map to the headers
        row_data = _convert_row_data_to_dict(matched_row_content, headers)
        rows.append(row_data)
        # Remove the content
        table_data = row_pattern.sub('', table_data, 1)
    return rows


def _convert_row_data_to_dict(row_data: str, headers: list[str]) -> list:
    """
    Converts the row data into proper cells and maps them to the header
    """
    td_content_pattern = re.compile('<td class="gradeA">(.*?)</td>')
    parsed_row = []
    while True:
        matches = td_content_pattern.search(row_data)
        if not matches or len(matches.groups()) == 0:
            break
        # Map this with the headers when adding
        cell_content = _strip_html_tags(matches.groups()[0])
        parsed_row.append(cell_content)
        row_data = td_content_pattern.sub('', row_data, 1)
    return parsed_row

def _strip_html_tags(source_text:str) -> str:
    """
    Strips all the HTML tags and stuff from the given string
    """
    html_tag_pattern = r"<[^>]*>"
    no_html_string = re.sub(html_tag_pattern, ' ', source_text)
    # We also have to replace the &nbsp; sequence with nothing.
    no_special_space_string = re.sub('&nbsp;', ' ', no_html_string).strip()
    return no_special_space_string
    
    