from ..nodes.tag import tag


class h2(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, 'h2')
        if text is not None:
            self.create.node.content(text)
