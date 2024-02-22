import importlib
from datetime import datetime


class core:
    def __init__(self, session_id):
        self._session_id = session_id
        self._session_time_start = datetime.now()
        self._configs = None

    @property
    def session_id(self): return self._session_id
    @property
    def session_time_start(self): return self._session_time_start

    @property
    def configs(self):
        if self._configs is None:
            from .configs import configs
            self._configs = configs()
        return self._configs

    def http(self):
        # TODO 当前默认调用后台初始化文件
        name = 'root.projects.default.applications.default.modules.default.index'
        name1 = 'hebill.libraries.hebill_system.initialize.root.projects.default.applications.default.modules.default.index'

        try:
            module = importlib.import_module(name)
            index = module.index
        except ImportError as e:
            module = importlib.import_module(name1)
            index = module.index

        # TODO 当前默认执行 default->default->default
        from hebill.libraries.hebill_system.core import x
        ind = index(x.jun_project_core('default').jun_application_core('default').jun_module_core('default'))
        return ind.http()
