from typing import List

from ds_simple_db.core.entry import Entry
from ds_simple_db.core.serializer import Serializer


class HTMLSerializer(Serializer):
    def __init__(self, border=1):
        self._border = border

    def entries_to_string(self, entries: List[Entry]) -> str:
        """
        Serialize entry list into a simple HTML table

        :param entries:
        :return:
        """
        if len(entries) == 0:
            return ''

        out_str = f'<table border="{self._border}">'

        out_str += self._get_header(entries[0].fields())

        for entry in entries:
            out_str += self._get_row(entry.values())

        out_str += '</table>'

        return out_str

    def entries_from_string(self, input_str: str) -> List[Entry]:
        raise NotImplementedError("Deserialization of HTML not implemented")

    def _get_header(self, fields):
        """
        Generate a header

        :param fields:
        :return:
        """
        out_str = '<tr>'

        for value in fields:
            out_str += '<th>'
            out_str += value
            out_str += '</th>'

        out_str += '</tr>'

        return out_str

    def _get_row(self, values):
        """
        Generate a row

        :param values:
        :return:
        """
        out_str = '<tr>'

        for value in values:
            out_str += '<td>'
            out_str += value
            out_str += '</td>'

        out_str += '</tr>'

        return out_str
