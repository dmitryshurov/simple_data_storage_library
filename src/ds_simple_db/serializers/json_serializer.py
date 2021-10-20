import json
from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.core.serializer import Serializer


class JSONSerializer(Serializer):
    """
    Serializer to a JSON format with a given `indent`.
    The behaviour is similar to Python standard `json.dumps()`.
    """
    def __init__(self, indent: int = None):
        self._indent = indent

    def entries_to_string(self, entries: List[Entry]) -> str:
        """
        Serialise JSON to a string using a standard Python standard `json.dumps()` function.

        :param entries: A list of entries to serialize
        :return: A serialized JSON string
        """
        entries_data = []

        for entry in entries:
            entries_data.append(entry.as_dict())

        return json.dumps(dict(entries=entries_data), indent=self._indent)

    def entries_from_string(self, input_str: str) -> List[Entry]:
        """
        Deserialize JSON from a string using a standard Python standard `json.loads()` function.

        The format of the input must be as follows:
        {"entries": [{"field1": "value1", "field2": "value2"}]}

        :param input_str: A JSON string to serialize
        :return: A list of entries deserialized from a string
        """
        entries = []

        data_dict = json.loads(input_str)

        if 'entries' not in data_dict:
            raise ValueError('Input string must be of format: {"entries": [{"field1": "value1", "field2": "value2"}]}')

        for entry_data in data_dict['entries']:
            entry = Entry(data=entry_data)
            entries.append(entry)

        return entries
