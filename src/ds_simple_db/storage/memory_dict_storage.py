from copy import deepcopy
from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.core.filter import Filter
from ds_simple_db.core.storage import Storage


class MemoryDictStorage(Storage):
    """
    This is an in-memory storage using standard Python dictionary that has no persistent representation.

    Note that internally it keeps columns as keys and values as lists for efficiency.
    """

    def __init__(self, initial_data: dict = None, columns: list = None):
        if initial_data is None and columns is None:
            self._data = dict()

        elif initial_data is not None and columns is None:
            self._validate_data(initial_data)

            # We want a deepcopy here to prevent occasional modifications of the storage from outside
            self._data = deepcopy(initial_data)

        elif columns is not None and initial_data is None:
            self._data = self._initialize_data_with_columns(columns)

        else:
            raise ValueError('Either `initial_data` or `columns` can be provided, but not both')

    def __repr__(self):
        return str(self._data)

    def columns(self) -> list:
        """
        Get all columns present in the storage

        :return: A list of columns of the storage
        """
        return list(self._data.keys())

    def insert(self, **kwargs) -> Entry:
        """
        Insert an entry to the storage by appending values to the columns lists.
        Validate before insertion and raise exception in advance, thus preserving invariants (lengths of column lists).

        TODO: Wrapping this function into a mutex should be considered for thread-safety

        :return: Inserted Entry
        """

        # Validate columns before insertion
        for column in kwargs.keys():
            if column not in self._data:
                raise ValueError(f'Column `{column}` does not exist in the storage')

        # Track the columns that are being inserted to figure out which were not present in data
        non_inserted_columns = self.columns()

        for column, value in kwargs.items():
            self._data[column].append(value)
            non_inserted_columns.remove(column)

        if len(non_inserted_columns) == len(self.columns()):
            raise ValueError('Can not perform insertion because empty data provided')

        # Fill remaining columns with None values
        for column in non_inserted_columns:
            self._data[column].append(None)

        return self._entry_by_index(-1)

    def all_entries(self) -> List[Entry]:
        if len(self.columns()) == 0:
            return []

        num_entries = len(self._data[self.columns()[0]])

        all_entries = list()

        for idx in range(num_entries):
            entry = self._entry_by_index(idx)
            all_entries.append(entry)

        return all_entries

    def filter(self, filter_obj: Filter = None) -> List[Entry]:
        if filter_obj is None:
            return []

        if not isinstance(filter_obj, Filter):
            raise TypeError(f'filter must be of type `Filter`, got {type(filter_obj)}')

        return [entry for entry in self.all_entries() if filter_obj.satisfies(entry)]

    def _entry_by_index(self, idx):
        """
        Get an entry by its index

        :param idx: The entry index
        :return: Entry
        """
        entry_data = dict()

        for column in self.columns():
            entry_data[column] = self._data[column][idx]

        return Entry(entry_data)

    @staticmethod
    def _validate_data(data):
        if not isinstance(data, dict):
            raise TypeError(f'MemoryDictStorage `initial_data` must be of type `dict`, got {type(data)}')

        list_length = None

        for _, val in data.items():
            if not isinstance(val, list):
                raise TypeError(f'MemoryDictStorage `initial_data` values must be of type `list`, got {type(val)}')

            if list_length is None:
                list_length = len(val)

            elif list_length != len(val):
                raise ValueError('Lengths of data columns do not match')

    @staticmethod
    def _initialize_data_with_columns(columns):
        data = dict()

        for column in columns:
            data[column] = list()

        return data
