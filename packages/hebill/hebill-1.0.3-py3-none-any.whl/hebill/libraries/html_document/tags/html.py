from ..nodes.tag import tag


class html(tag):
    def __init__(self, senior, lang: str = None):
        super().__init__(senior, 'html')
        if lang is not None:
            self.attributes["lang"] = lang