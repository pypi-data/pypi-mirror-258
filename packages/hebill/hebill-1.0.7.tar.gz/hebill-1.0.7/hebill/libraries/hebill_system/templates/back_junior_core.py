import os.path
from .back_node_core import back_node_core
from ..__constants__ import CONFIGS_FILE_NAME, TRANSLATIONS_DIR_NAME, CONFIGS_DICT_NAME, CN_LANGUAGE


class back_junior_core(back_node_core):
    def __init__(self, x_file, senior, name, path=None):
        super().__init__(x_file, senior, name, path)
        self._x_configs_file_path = None
        self._configs_file_path = None
        self._x_translations_dir_path = None
        self._translations_dir_path = None
        self._configs = None
        self._x_translations = None
        self._translations = None

    @property
    def x_configs_file_path(self):
        if self._x_configs_file_path is None:
            self._x_configs_file_path = os.path.join(self.x_path, CONFIGS_FILE_NAME)
        return self._x_configs_file_path

    @property
    def configs_file_path(self):
        if self._configs_file_path is None:
            self._configs_file_path = os.path.join(self.path, CONFIGS_FILE_NAME)
        return self._configs_file_path

    @property
    def configs(self):
        if self._configs is None:
            from ...multiple_configs.multiple_configs import multiple_configs
            self._configs = multiple_configs(self.x_configs_file_path, self.configs_file_path, CONFIGS_DICT_NAME,
                                             CONFIGS_DICT_NAME)
        return self._configs

    @property
    def x_translations_dir_path(self):
        if self._x_translations_dir_path is None:
            self._x_translations_dir_path = os.path.join(self.x_path, TRANSLATIONS_DIR_NAME)
        return self._x_translations_dir_path

    @property
    def translations_dir_path(self):
        if self._translations_dir_path is None:
            self._translations_dir_path = os.path.join(self.path, TRANSLATIONS_DIR_NAME)
        return self._translations_dir_path

    @property
    def x_translations(self):
        if self._x_translations is None:
            from ...multiple_translations.multiple_translations import multiple_translations
            self._x_translations = multiple_translations(self.x_translations_dir_path,
                                                         self.configs.system.get(CN_LANGUAGE),
                                                         self.configs.default.get(CN_LANGUAGE),
                                                         self.configs.user.get(CN_LANGUAGE))
        return self._x_translations

    @property
    def translations(self):
        if self._translations is None:
            from ...multiple_translations.multiple_translations import multiple_translations
            self._translations = multiple_translations(self.translations_dir_path,
                                                       self.configs.system.get(CN_LANGUAGE),
                                                       self.configs.default.get(CN_LANGUAGE),
                                                       self.configs.user.get(CN_LANGUAGE))
        return self._translations
