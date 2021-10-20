from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.core.serializer import Serializer


class CSVSerializer(Serializer):
    """
    Serializer to a CSV format with a given `delimiter` and `newline`.

    Sample output:
        #name,address\n
        Dmitry,Moscow\n
        Andrew,London\n
    """

    def __init__(self):
        self._delimiter = ','
        self._newline = '\n'

    def entries_to_string(self, entries: List[Entry]) -> str:
        """
        Serialise CSV to a string in a following CSV format:

        #header_col1,header_col2\n
        entry1_field1,entry1_field2\n
        entry2_field1,entry2_field2\n

        Commas here can be replaced by any delimiter given in a CSVSerializer constructor
        Newline delimiter can also be set in a CSVSerializer constructor

        Note that no typing is provided at the moment so all values will be considered as strings.
        Thus we explicitly prohibit serializing non-string values to avoid any deserialization incoherence.

        :param entries: A list of entries to serialize
        :return: A serialized string
        """
        if len(entries) == 0:
            return ''

        # Write header
        first_entry_fields = entries[0].fields()
        entries_data = '#' + self._make_line(first_entry_fields)

        # Write values
        for entry in entries:
            self._check_entry_fields_match(first_entry_fields, entry.fields())
            entries_data += self._make_line(entry.values())

        return entries_data

    def entries_from_string(self, input_str: str) -> List[Entry]:
        """
        Deserialize CSV from a string using a standard Python standard `json.loads()` function.

        Note that no typing is provided at the moment so all values will be considered as strings.

        The format of the input must be as follows:
        #header_col1,header_col2\n
        entry1_field1,entry1_field2\n
        entry2_field1,entry2_field2\n

        :param input_str: A CSV string to serialize
        :return: A list of entries deserialized from a string
        """
        lines = input_str.splitlines()
        header = self._get_header(lines)
        entries = self._get_entries(header, lines)

        return entries

    def _get_header(self, lines):
        if len(lines) == 0:
            raise ValueError('Header not found in the input')

        header_line = lines[0]

        if not header_line.startswith('#'):
            raise ValueError('Header must start with #')

        header_line_without_hash = header_line[1:]
        header = self._split_line(header_line_without_hash)

        return header

    def _get_entries(self, header, lines):
        entries = []

        for line in lines:
            if line.startswith('#'):
                continue

            values = self._split_line(line)

            if len(values) != len(header):
                raise ValueError('Number of tokens in a line does not match the header')

            entry_data = dict(zip(header, values))
            entry = Entry(data=entry_data)
            entries.append(entry)

        return entries

    def _split_line(self, line):
        return [x.strip() for x in line.split(',')]

    def _make_line(self, tokens: List[str]) -> str:
        """
        Make a single line of a csv file given a list of string tokens.

        Tokens are joined using a `delimiter` and the whole line appended with a `newline`.

        Can be used to create both header and data lines.

        None values are converted to empty strings

        :param tokens: A list of string tokens to join using a given delimiter
        :return: A resulting CSV line
        """
        values = [self._handle_type(x) for x in tokens]
        return self._delimiter.join(values) + self._newline

    def _handle_type(self, token):
        """
        Do type conversion

        TODO: this potentially should be much more elaborated than the current implementation

        :param token: Input token with source type
        :return: Converted token with type consideration
        """
        return token if token is not None else ''

    @staticmethod
    def _check_entry_fields_match(first_entry_fields: List[str], entry_fields: List[str]):
        """
        Check if entry field set match and raise ValueError if not

        :param first_entry_fields: Entry fields of a first entry
        :param entry_fields: Entry fields of another entry
        """
        if entry_fields != first_entry_fields:
            raise ValueError('Entries have different sets of fields')
