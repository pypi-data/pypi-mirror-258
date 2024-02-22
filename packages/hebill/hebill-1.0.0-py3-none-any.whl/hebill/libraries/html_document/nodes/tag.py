import uuid

from .group import group


class tag(group):
    def __init__(self, senior, name: str):
        super().__init__(senior)
        self.name = name
        self.attributes: dict = {}
        self.output_breakable = True

    def output(self):
        s = ""
        if self.document.output_break:
            if self.output_breakable and self.document.output_next_breakable:
                if self.node_level > 0:
                    s += "\n"
            s += self.document.output_retraction * self.node_level
        s += "<" + self.name
        if len(self.attributes) > 0:
            for n, v in self.attributes.items():
                s += f" {n}=\"{v}\""
        s += ">"
        self.document.output_next_breakable = True
        si = super().output()
        s += si
        if self.document.output_break:
            if si != "" and self.document.output_next_breakable:
                s += "\n" + "	" * self.node_level
        s += "</" + self.name + ">"
        self.document.output_next_breakable = True
        return s

    def _attribute_x(self, name: str, value: int | float | str | bool = None):
        if value is not None:
            self.attributes[name] = value
        if name in self.attributes:
            return self.attributes[name]
        if name == 'id':
            self.attributes[name] = str(uuid.uuid4()).replace('-', '')
            return self.attributes[name]
        return None

    @property
    def attribute_id(self): return self._attribute_x('id')

    @attribute_id.setter
    def attribute_id(self, uid): self._attribute_x('id', uid)

    @property
    def attribute_name(self): return self._attribute_x('name')

    @attribute_name.setter
    def attribute_name(self, name): self._attribute_x('name', name)
