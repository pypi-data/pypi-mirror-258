class _create_tags:
    def __init__(self, senior):
        self.senior = senior

    def a(self, title: str = None, url: str = None):
        from ...tags.a import a
        return a(self.senior, title, url)

    def body(self):
        from ...tags.body import body
        return body(self.senior)

    def div(self, text: str = None):
        from ...tags.div import div
        return div(self.senior, text)

    def h1(self, text: str = None):
        from ...tags.h1 import h1
        return h1(self.senior, text)

    def h2(self, text: str = None):
        from ...tags.h2 import h2
        return h2(self.senior, text)

    def h3(self, text: str = None):
        from ...tags.h3 import h3
        return h3(self.senior, text)

    def h4(self, text: str = None):
        from ...tags.h4 import h4
        return h4(self.senior, text)

    def h5(self, text: str = None):
        from ...tags.h5 import h5
        return h5(self.senior, text)

    def h6(self, text: str = None):
        from ...tags.h6 import h6
        return h6(self.senior, text)

    def head(self):
        from ...tags.head import head
        return head(self.senior)

    def html(self, lang: str = None):
        from ...tags.html import html
        return html(self.senior, lang)

    def input_text(self, name: str = None, value: str | int | float = None, placeholder: str = None):
        from ...tags.input_text import input_text
        return input_text(self.senior, name, value, placeholder)

    def link(self, url: str = None):
        from ...tags.link import link
        return link(self.senior, url)

    def script(self, url: str = None):
        from ...tags.script import script
        return script(self.senior, url)

    def span(self, text: str = None):
        from ...tags.span import span
        return span(self.senior, text)

    def table(self):
        from ...tags.table import table
        return table(self.senior)

    def tbody(self):
        from ...tags.tbody import tbody
        return tbody(self.senior)

    def th(self):
        from ...tags.th import th
        return th(self.senior)

    def td(self):
        from ...tags.td import td
        return td(self.senior)

    def thead(self):
        from ...tags.thead import thead
        return thead(self.senior)

    def title(self, text: str = None):
        from ...tags.title import title
        return title(self.senior, text)

    def tr(self):
        from ...tags.tr import tr
        return tr(self.senior)
