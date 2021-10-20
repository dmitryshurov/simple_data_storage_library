from unittest import TestCase

from ds_simple_db.core.entry import Entry
from ds_simple_db.serializers.table_serializer import TableSerializer


class TestTableSerializer(TestCase):
    def test_entries_to_string_empty_entries_returns_empty_string(self):
        entries = []

        self.assertEqual(
            '',
            TableSerializer().entries_to_string(entries)
        )

    def test_row_separator(self):
        self.assertEqual(
            '+-----+-----+\n',
            TableSerializer(row_width=5)._get_row_separator(num_cols=2)
        )

        self.assertEqual(
            '+---+\n',
            TableSerializer(row_width=3)._get_row_separator(num_cols=1)
        )

    def test_get_row_content(self):
        values = ['col', 'value', 'col3']

        self.assertEqual(
            '| col |value|col3 |\n',
            TableSerializer(row_width=5)._get_row_content(values)
        )

        self.assertEqual(
            '|col|val|col|\n',
            TableSerializer(row_width=3)._get_row_content(values)
        )

    def test_get_header(self):
        cols = ['col', 'value', 'col3']

        self.assertEqual(
            '+-----+-----+-----+\n| col |value|col3 |\n+-----+-----+-----+\n',
            TableSerializer(row_width=5)._get_header(cols)
        )

    def test_get_row(self):
        cols = ['col', 'value', 'col3']

        self.assertEqual(
            '| col |value|col3 |\n+-----+-----+-----+\n',
            TableSerializer(row_width=5)._get_row(cols)
        )

    def test_entries_to_string(self):
        entries = [
            Entry(data=dict(col='val', value='field', col3='val3')),
        ]

        self.assertEqual(
            '+-----+-----+-----+\n| col |value|col3 |\n+-----+-----+-----+\n| val |field|val3 |\n+-----+-----+-----+\n',
            TableSerializer(row_width=5).entries_to_string(entries)
        )
