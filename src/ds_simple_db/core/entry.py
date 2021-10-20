from copy import deepcopy


class Entry:
    """
    A storage entry.

    Entries are intended to represent data that is inserted or retrieved from the storage.
    Each entry contains fields and their corresponding values.

    The current internal data structure for storing entry data is a default dictionary,
    but clients should not rely on that as it may be subject to a change
    """

    def __init__(self, data: dict = None):
        """
        Construct an entry from a given data dictionary

        :param data: Data dict to initialize
        """
        if data is None:
            self._data = dict()

        elif not isinstance(data, dict):
            raise TypeError(f'Data must be of type `dict`, {type(data)} given')

        else:
            self._data = deepcopy(data)

    def fields(self):
        """
        Get a list of fields in entry

        :return: A list of entry fields
        """
        return list(self._data.keys())

    def values(self):
        """
        Get a list of field values in entry.
        Must be ordered the same way as fields().

        :return: A list of entry values
        """
        return list(self._data.values())

    def as_dict(self):
        """
        Return entry representation as a dictionary

        :return: A representation of internal data as a dictionary
        """
        return deepcopy(self._data)

    def __repr__(self):
        return 'Entry: ' + str(self.as_dict())

    def __getitem__(self, item):
        """
        Get a value of a given column.
        Raise ValueError is column does not exist

        :param item: A field name
        :return: A field value
        """
        if item not in self.fields():
            raise ValueError(f'Column `{item}` does not exist in the Entry')

        return self._data[item]

    def __getattr__(self, item):
        """
        A shortcut for __getitem__ to provide a Pythonic way to access columns

        :param item: A field name
        :return: A field value
        """
        return self[item]

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    def __ne__(self, other):
        return not self == other
