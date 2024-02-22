from .single_configs_by_file import single_configs_by_file
from .single_configs_by_empty import single_configs_by_empty


class multiple_configs:
    def __init__(self, sys_file: str, def_file: str, sys_module: str = "configs", def_module: str = "configs"):
        self._sys_file = sys_file
        self._def_file = def_file
        self._sys_module = sys_module
        self._def_module = def_module
        self._system = None
        self._default = None
        self._user = None

    @property
    def system(self) -> single_configs_by_file:
        if self._system is None:
            self._system = single_configs_by_file(self._sys_file, self._sys_module)
        return self._system

    @property
    def default(self) -> single_configs_by_file:
        if self._default is None:
            self._default = single_configs_by_file(self._def_file, self._def_module)
        return self._default

    @property
    def user(self) -> single_configs_by_empty:
        if self._user is None:
            self._user = single_configs_by_empty()
        return self._user

    def get(self, key: str) -> str | None:
        result = self.user.get(key)
        if result is not None:
            return result
        result = self.default.get(key)
        if result is not None:
            return result
        result = self.system.get(key)
        if result is not None:
            return result
        return None
