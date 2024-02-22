from ....multiple_configs.multiple_configs import multiple_configs as multiple_configs_tpl
from .single_configs_by_file import single_configs_by_file
from .single_configs_by_empty import single_configs_by_empty
from ...__constants__ import CONFIGS_DICT_NAME
from .common import common


class multiple_configs(multiple_configs_tpl, common):
    def __init__(self, sys_file: str, def_file: str):
        super().__init__(sys_file, def_file, CONFIGS_DICT_NAME, CONFIGS_DICT_NAME)

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
