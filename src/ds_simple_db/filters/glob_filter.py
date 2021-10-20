from fnmatch import fnmatch

from ds_simple_db.core.entry import Entry
from ds_simple_db.core.filter import Filter


class GlobFilter(Filter):

    def __init__(self, filter_str: str):
        if not isinstance(filter_str, str):
            raise TypeError(f'filter_str must be of type `str`, `{type(filter_str)}` given')

        self._field, self._pattern = self._get_field_and_pattern(filter_str)
        self._filter_str = filter_str

    def satisfies(self, entry: Entry) -> bool:
        return fnmatch(str(entry[self._field]), self._pattern)

    @staticmethod
    def _get_field_and_pattern(filter_str):
        tokens = filter_str.split('=')

        if len(tokens) != 2 or len(tokens[0]) == 0 or len(tokens[1]) == 0:
            raise ValueError(f'`filter_str` must contain exactly one pair `column=pattern`, `{filter_str}` given')

        return tokens

    def __repr__(self):
        return self._filter_str
