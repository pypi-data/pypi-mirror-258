class create:
    def __init__(self, senior):
        self.senior = senior
        self._nodes = None
        self._tags = None
        self._components = None

    @property
    def node(self):
        if self._nodes is None:
            from .create_nodes import _create_nodes
            self._nodes = _create_nodes(self.senior)
        return self._nodes

    @property
    def tag(self):
        if self._tags is None:
            from .create_tags import _create_tags
            self._tags = _create_tags(self.senior)
        return self._tags

    @property
    def component(self):
        if self._components is None:
            from .create_components import _create_components
            self._components = _create_components(self.senior)
        return self._components
