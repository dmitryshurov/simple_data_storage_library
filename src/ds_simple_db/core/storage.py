import os
from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.core.filter import Filter
from ds_simple_db.serializers import SerializerFactory


class Storage:
    """
    A base class for all storage types that provide underlying structures to store data.
    Storage can be persistent (e.g., databases) or non-persistent (in-memory).

    In general, a Storage subclasses can even represent a combination of multiple other ModelStorage subclasses
    to provide a synchronized multi-storage architecture.
    """

    def insert(self, data_dict: dict) -> Entry:
        """
        Insert a value to the storage.
        This operation, depending on implementation, does not necessarily commit a change to the actual storage.
        Some storage types may use an internal cache to optimize write operations.

        :param data_dict: An dictionary containing data to insert
        :return: Inserted Entry
        """
        pass

    def columns(self) -> list:
        """
        Get all columns present in the storage

        :return: A list of columns of the storage
        """
        pass

    def all_entries(self) -> List[Entry]:
        """
        Retrieve all entries in the storage

        :return: A list of all entries in the storage
        """
        pass

    def filter(self, filter_obj: Filter) -> List[Entry]:
        """
        Retrieve the data from the storage using a given filter.
        An empty filter must return an empty list

        :param filter_obj: A filter to apply to the storage entries
        :return: A list of filtered entries
        """
        pass

    def load_from_file(self, db_path):
        """
        Load (deserialize) a storage from a file

        The type of serializer is inferred from the file extension using SerializerFactory

        Note that this does not clear the storage, so you can load multiple files into the storage

        :param db_path: Path to a file to deserialize data from
        :return:
        """
        if not os.path.exists(db_path):
            raise ValueError(f"File `{db_path}` does not exist")

        with open(db_path, 'r') as fp:
            raw_data_str = fp.read()

        serializer = self._get_serializer_from_file_name(db_path)
        deserialized_data = serializer.entries_from_string(raw_data_str)

        for entry in deserialized_data:
            self.insert(**entry.as_dict())

    def save_to_file(self, db_path):
        """
        Save (serialize) the storage to a file

        The type of serializer is inferred from the file extension using SerializerFactory

        :param db_path: Path to a file to serialize data to
        :return:
        """
        serializer = self._get_serializer_from_file_name(db_path)
        serialized_data = serializer.entries_to_string(self.all_entries())

        db_folder = os.path.dirname(db_path)

        if not os.path.exists(db_folder):
            os.makedirs(db_folder)

        with open(db_path, 'w') as fp:
            fp.write(serialized_data)

    def _get_serializer_from_file_name(self, db_path):
        db_format = db_path.split('.')[-1]
        serializer = SerializerFactory.create(db_format)

        return serializer
