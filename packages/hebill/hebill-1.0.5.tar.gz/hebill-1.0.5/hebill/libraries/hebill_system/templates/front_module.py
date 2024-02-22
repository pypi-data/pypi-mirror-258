from ..system.projects.project.applications.application.modules.module.core import core


class front_module:
    def __init__(self, x):
        self._x: core = x

    @property
    def x(self) -> core: return self._x
