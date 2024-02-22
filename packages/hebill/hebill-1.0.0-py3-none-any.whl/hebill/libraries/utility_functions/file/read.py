def read(path: str):
    from .is_readable import is_readable
    if not is_readable(path):
        return ""
    with open(path, 'r') as file:
        return file.read()
