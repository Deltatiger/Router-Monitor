def ljust(data: str, width: int) -> str:
    """
    Makes the string the required width
    """
    if len(data) >= width:
        # TODO Should this be truncated in the case that it is longer ?
        return data
    return ' ' * (width - len(data)) + data

def strip_newlines(text: str) -> str:
    """
    Strips all the newline characters in the string
    """
    # TODO This might be costly. If not required, optimize
    lines = text.split('\n')
    return ''.join(line.strip() for line in lines)