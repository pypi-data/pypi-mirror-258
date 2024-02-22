def from_ini_file(file: str) -> dict:
    import configparser
    loader = configparser.ConfigParser()
    try:
        loader.read_string("[DEFAULT]\n" + open(file, encoding='utf-8').read())
        result = dict(loader['DEFAULT'])
    except (FileNotFoundError, configparser.Error):
        result = {}
    return result
