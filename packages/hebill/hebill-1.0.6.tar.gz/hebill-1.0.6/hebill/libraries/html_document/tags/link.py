from ..nodes.tag import tag


class link(tag):
    def __init__(self, senior, url: str = None):
        super().__init__(senior, 'link')
        if url is not None:
            self.attributes["href"] = url
