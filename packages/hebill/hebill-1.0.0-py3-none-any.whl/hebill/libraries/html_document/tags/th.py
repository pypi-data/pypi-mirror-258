from ..nodes.tag import tag


class th(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, 'th')
        if text is not None:
            self.create.node.content(text)
        