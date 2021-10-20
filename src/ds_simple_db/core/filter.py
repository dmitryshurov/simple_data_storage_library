from ds_simple_db.core.entry import Entry


class Filter:
    """
    The base class for all filters.

    To implement a new filter you need to implement the following methods:
        * satisfies
    """

    def satisfies(self, entry: Entry) -> bool:
        """
        Check if an entry satisfies the filter

        :param entry: An entry to check if it satisfies the filter
        :return: True if entry satisfies the filter, False otherwise
        """
        pass
