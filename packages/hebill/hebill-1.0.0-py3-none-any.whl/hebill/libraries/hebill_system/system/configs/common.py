from ...__constants__ import *


class common:
    def get(self, name):
        pass

    def get_language(self):
        return self.get(CN_LANGUAGE)

    def get_url_name_target(self):
        return self.get(CN_UN_TARGET)

    def get_url_name_language(self):
        return self.get(CN_UN_ARGUMENTS)

    def get_url_name_method(self):
        return self.get(CN_UN_METHOD)

    def get_url_name_search(self):
        return self.get(CN_UN_SEARCH)

    def get_url_name_search_keyword(self):
        return self.get(CN_UN_SEARCH_KEYWORD)

    def get_url_name_search_page(self):
        return self.get(CN_UN_SEARCH_PAGE)

    def get_url_name_search_orders(self):
        return self.get(CN_UN_SEARCH_ORDERS)

    def get_url_name_search_filters(self):
        return self.get(CN_UN_SEARCH_FILTERS)

    def get_url_name_search_items_per_page(self):
        return self.get(CN_UN_SEARCH_ITEMS_PER_PAGE)

    def get_url_name_search_pages_per_group(self):
        return self.get(CN_UN_SEARCH_PAGES_PER_GROUP)
