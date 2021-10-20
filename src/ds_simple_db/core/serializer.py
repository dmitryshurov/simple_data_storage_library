from typing import List

from ds_simple_db.core.entry import Entry


class Serializer:
    """
    The base class for all serializers.

    To implement a new serializer you need to implement the following methods:
        * entries_to_string (serialize a list of entries to a string)
        * entries_from_string (deserialize a list of entries from a string)
    """

    def entries_to_string(self, entries: List[Entry]) -> str:
        """
        Dump a list of entries to a string.
        This must be implemented in a derived class to support serialization

        :param entries: A list of entries to serialize
        :return: A serialized string
        """
        pass

    def entries_from_string(self, input_str: str) -> List[Entry]:
        """
        Load a list of entries from a string.
        This must be implemented in a derived class to support deserialization

        :param input_str: A string to serialize
        :return: A list of entries deserialized from a string
        """
        pass
