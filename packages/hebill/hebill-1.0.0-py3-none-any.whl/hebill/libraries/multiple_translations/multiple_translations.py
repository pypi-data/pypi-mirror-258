import os.path

from .single_translations import single_translations


class multiple_translations:
    def __init__(self, path: str, sys_language: str = None, def_language: str = None, usr_language: str = None):
        self._path = path
        self._sys_langauge = sys_language
        self._def_langauge = def_language
        self._usr_langauge = usr_language
        self._packages = {}

    @property
    def path(self) -> str:
        return self._path

    @property
    def zhCN(self):
        return self.package('zh-CN')

    @property
    def enGB(self):
        return self.package('en-GB')

    @property
    def system_language(self) -> str:
        return self._sys_langauge

    @property
    def default_langauge(self) -> str:
        return self._def_langauge

    @property
    def user_language(self) -> str:
        return self._usr_langauge

    def package(self, langauge: str = None) -> single_translations:
        if langauge is None:
            langauge = "_"
        if langauge not in self._packages:
            self._packages[langauge] = single_translations(os.path.join(self.path, langauge + ".ini"))
        return self._packages[langauge]

    @property
    def package_system(self) -> single_translations:
        return self.package(self.system_language)

    @property
    def package_default(self) -> single_translations:
        return self.package(self.default_langauge)

    @property
    def package_user(self) -> single_translations:
        return self.package(self.user_language)

    def get(self, key: str) -> str:
        result = self.package_user.read(key)
        if result is not None:
            return result
        result = self.package_default.read(key)
        if result is not None:
            return result
        result = self.package_system.read(key)
        if result is not None:
            return result
        return key
