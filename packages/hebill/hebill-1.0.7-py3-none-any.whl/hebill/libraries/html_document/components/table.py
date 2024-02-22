from ..tags.table import table as table_parent_class
from .table_sub.thead import thead
from .table_sub.tbody import tbody


class table(table_parent_class):
    def __init__(self, senior):
        super().__init__(senior)
        self._head_wrap = self.create.node.group()
        self._head = None
        self._body = None

    @property
    def head(self) -> thead:
        if self._head is None:
            self._head = thead(self._head_wrap)
        return self._head

    @property
    def body(self) -> tbody:
        if self._body is None:
            self._body = tbody(self)
        return self._body

    def set_bordered(self):
        pass
