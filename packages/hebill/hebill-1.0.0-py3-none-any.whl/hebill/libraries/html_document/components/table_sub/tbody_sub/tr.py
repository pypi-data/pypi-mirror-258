from ....tags.tr import tr as tr_parent_class
from .tr_sub.td import td


class tr(tr_parent_class):
    def __init__(self, senior):
        super().__init__(senior)
        self._cells = []
        self._cell = None

    @property
    def cells(self) -> list:
        return self._cells

    @property
    def cell(self) -> td:
        if self._cell is None:
            self.add_cell()
        return self._cell

    def add_cell(self, text: str = None) -> td:
        self._cell = td(self, text)
        self._cells.append(self._cell)
        return self._cell
