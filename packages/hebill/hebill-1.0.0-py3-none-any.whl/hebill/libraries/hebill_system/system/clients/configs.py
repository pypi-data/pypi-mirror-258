from ....multiple_configs.single_configs_by_empty import single_configs_by_empty


class configs(single_configs_by_empty):
    @property
    def language(self): return self.get('language')

    @language.setter
    def language(self, langauge): self.set('language', langauge)
