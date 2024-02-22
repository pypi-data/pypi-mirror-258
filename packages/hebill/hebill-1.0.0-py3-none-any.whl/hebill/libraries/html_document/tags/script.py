from ..nodes.tag import tag


class script(tag):
    def __init__(self, senior, url: str = None):
        super().__init__(senior, 'script')
        if url is not None:
            self.attributes["src"] = url
