import json

def read_configuration(config_file_path: str) -> dict:
    """
    Read the configuration JSON and load it into memory
    """
    try:
        with open(config_file_path) as f:
            config = json.loads(''.join(f.readlines()))
            return config
    except Exception as e:
        print('Cannot read the configuration file. Aborting.')
        print(e)
        sys.exit(-1)