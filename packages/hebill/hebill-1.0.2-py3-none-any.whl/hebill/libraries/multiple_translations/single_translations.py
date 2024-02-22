class single_translations:
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._cache = None
        self.load()

    @property
    def path(self):
        return self._path

    def load(self) -> bool:
        from ..utility_functions.file.import_dict.from_ini_file import from_ini_file
        r = from_ini_file(self.path)
        self._cache = r
        return True

    @property
    def all(self) -> dict:
        return self._cache

    def get(self, key: str) -> str:
        r = self.read(key)
        if r is not None:
            return r
        return key

    def read(self, key: str) -> str | None:
        return self._cache.get(key)
