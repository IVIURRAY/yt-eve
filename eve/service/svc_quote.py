from quote import quote
import random
from textwrap import shorten, wrap
from eve.config import QU_SEARCH


class Quote:
    def __init__(self):
        self.default_search = QU_SEARCH

    def random(self, search):
        results = quote(search or self.default_search)
        if not results:
            return ""
        random_quote = random.choice(results)["quote"]
        wrapped_quote = "\n".join(wrap(shorten(random_quote, 280 - 4, placeholder="..."), 70))
        return wrapped_quote
