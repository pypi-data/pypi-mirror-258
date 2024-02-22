from ...tags.head import head as head_parent_class
from .head_sub.title import title


class head(head_parent_class):
    def __init__(self, senior):
        super().__init__(senior)
        self._metas = self.create.node.group()
        self._libraries = self.create.node.group()
        self._title = title(self)

    @property
    def metas(self):
        return self._metas.create.tag.title()

    @property
    def libraries(self):
        return self._libraries

    @property
    def title(self):
        return self._title

