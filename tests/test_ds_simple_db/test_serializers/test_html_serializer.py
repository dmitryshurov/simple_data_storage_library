from unittest import TestCase

from ds_simple_db.core.entry import Entry
from ds_simple_db.serializers.html_serializer import HTMLSerializer


class TestHTMLSerializer(TestCase):
    def test_entries_to_string_empty_entries_returns_empty_string(self):
        entries = []

        self.assertEqual(
            '',
            HTMLSerializer().entries_to_string(entries)
        )

    def test_get_header(self):
        cols = ['col', 'value', 'col3']

        self.assertEqual(
            '<tr><th>col</th><th>value</th><th>col3</th></tr>',
            HTMLSerializer()._get_header(cols)
        )

    def test_get_row(self):
        cols = ['col', 'value', 'col3']

        self.assertEqual(
            '<tr><td>col</td><td>value</td><td>col3</td></tr>',
            HTMLSerializer()._get_row(cols)
        )

    def test_entries_to_string(self):
        entries = [
            Entry(data=dict(col='val', value='field', col3='val3')),
        ]

        self.assertEqual(
            '<table border="1">'
            '<tr><th>col</th><th>value</th><th>col3</th></tr><tr>'
            '<td>val</td><td>field</td><td>val3</td></tr>'
            '</table>',
            HTMLSerializer(border=1).entries_to_string(entries)
        )
