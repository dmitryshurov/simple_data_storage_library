from unittest import TestCase

from ds_simple_db.core.entry import Entry
from ds_simple_db.serializers.csv_serializer import CSVSerializer


class TestCsvSerializer(TestCase):
    def test_entries_to_string_empty_entries_returns_empty_string(self):
        entries = []

        self.assertEqual(
            '',
            CSVSerializer().entries_to_string(entries)
        )

    def test_entries_to_string_serializes_correctly(self):
        entries = [
            Entry(data=dict(col1='1', col2='str1')),
            Entry(data=dict(col1='2', col2='str2')),
        ]

        self.assertEqual(
            '#col1,col2\n1,str1\n2,str2\n',
            CSVSerializer().entries_to_string(entries)
        )

    def test_entries_to_string_none_is_converted_to_empty_string(self):
        entries = [
            Entry(data=dict(col1=None, col2='str1')),
            Entry(data=dict(col1='2', col2='str2')),
        ]

        self.assertEqual(
            '#col1,col2\n,str1\n2,str2\n',
            CSVSerializer().entries_to_string(entries)
        )

    def test_entries_to_string_raises_value_error_if_entry_fields_do_not_match(self):
        entries = [
            Entry(data=dict(col1='1')),
            Entry(data=dict(col1='2', col2='str2')),
        ]

        with self.assertRaises(ValueError):
            CSVSerializer().entries_to_string(entries)

    def test_entries_to_string_raises_type_error_if_value_is_not_str(self):
        entries = [
            Entry(data=dict(col1=1)),
            Entry(data=dict(col1='2', col2='str2')),
        ]

        with self.assertRaises(TypeError):
            CSVSerializer().entries_to_string(entries)

    def test_entries_from_string_deserializes_correctly(self):
        entries = [
            Entry(data=dict(col1='1', col2='str1')),
            Entry(data=dict(col1='2', col2='str2')),
        ]

        self.assertEqual(
            entries,
            CSVSerializer().entries_from_string(
                '#col1,col2\n1,str1\n2,str2\n'
            )
        )

    def test_entries_from_string_raises_value_error_if_empty_string(self):
        with self.assertRaises(ValueError):
            CSVSerializer().entries_from_string(
                '\n'
            )

    def test_entries_from_string_raises_value_error_if_header_not_starts_with_hash(self):
        with self.assertRaises(ValueError):
            CSVSerializer().entries_from_string(
                'col1,col2\n1,str1\n2,str2\n'
            )

    def test_entries_from_string_raises_value_error_if_line_does_not_match_header(self):
        with self.assertRaises(ValueError):
            CSVSerializer().entries_from_string(
                '#col1,col2\nval1,str1\nval2\n'
            )
