from ..html import html


class libraries:
    def __init__(self, htm):
        self._htm = htm
        self._files = []

    def add_js_file(self, url):
        if url not in self._files:
            self._files.append(url)
        pass

    def add_css_file(self, url):
        pass

    def use_hebill(self):
        pass

