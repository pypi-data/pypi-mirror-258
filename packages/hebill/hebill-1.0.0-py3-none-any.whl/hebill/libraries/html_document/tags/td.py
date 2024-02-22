from ..nodes.tag import tag


class td(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, 'td')
        if text is not None:
            self.create.node.content(text)
        