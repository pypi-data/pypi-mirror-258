from ..tags.html import html as html_parent_class
from .html_sub.head import head
from .html_sub.body import body


class html(html_parent_class):
    def __init__(self, senior, lang: str = None):
        super().__init__(senior, lang)
        self.__head = head(self)
        self.__body = body(self)

    @property
    def head(self):
        return self.__head

    @property
    def body(self):
        return self.__body

