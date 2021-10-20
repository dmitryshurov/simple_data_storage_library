from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.core.serializer import Serializer


class TableSerializer(Serializer):
    """
    Serialize an entry list to a string in a following format:

    +-------------+-------------+
    |  col1_name  |  col2_name  |
    +-------------+-------------+
    |  col1_value |  col2_value |
    +-------------+-------------+

    This is currently implemented only for serialisation/viewing purposes.
    No deserialization is supported.
    """

    def __init__(self, row_width: int = 20):
        self._row_width = row_width

    def entries_to_string(self, entries: List[Entry]) -> str:
        if len(entries) == 0:
            return ''

        cols = entries[0].fields()

        out_str = self._get_header(cols)

        for entry in entries:
            out_str += self._get_row(entry.values())

        return out_str

    def entries_from_string(self, input_str: str) -> List[Entry]:
        raise NotImplementedError("Deserialization of tables not implemented")

    def _get_row_separator(self, num_cols):
        col_str = '-' * self._row_width + '+'
        out_str = '+' + col_str * num_cols

        return out_str + '\n'

    def _get_row_content(self, values: List[str]):
        col_str = '|'

        for value in values:
            max_value_length = self._row_width

            if len(value) > max_value_length:
                value = value[:max_value_length]

            num_spaces = self._row_width - len(value)
            num_spaces_front = num_spaces // 2
            num_spaces_back = num_spaces - num_spaces_front

            formatted_value = ' ' * num_spaces_front + value + ' ' * num_spaces_back

            col_str += formatted_value + '|'

        return col_str + '\n'

    def _get_header(self, cols):
        row_separator = self._get_row_separator(num_cols=len(cols))
        out_str = row_separator
        out_str += self._get_row_content(cols)
        out_str += row_separator

        return out_str

    def _get_row(self, cols):
        row_separator = self._get_row_separator(num_cols=len(cols))
        out_str = self._get_row_content(cols)
        out_str += row_separator

        return out_str
