from ...tags.tbody import tbody as tbody_parent_class
from .tbody_sub.tr import tr


class tbody(tbody_parent_class):
    def __init__(self, senior):
        super().__init__(senior)
        self._rows = []
        self._row = None

    @property
    def rows(self) -> list:
        return self._rows

    @property
    def row(self) -> tr:
        if self._row is None:
            self.add_row()
        return self._row

    def add_row(self) -> tr:
        self._row = tr(self)
        self._rows.append(self._row)
        return self._row
