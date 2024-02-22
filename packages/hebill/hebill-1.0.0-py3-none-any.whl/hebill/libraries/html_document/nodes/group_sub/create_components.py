class _create_components:
    def __init__(self, senior):
        self.senior = senior

    def table(self):
        from ...components.table import table
        return table(self.senior)
