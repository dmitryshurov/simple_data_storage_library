from unittest import TestCase

from ds_simple_db.core.entry import Entry
from ds_simple_db.serializers.json_serializer import JSONSerializer


class TestJsonSerializer(TestCase):
    def test_entries_to_string_empty(self):
        entries = []

        self.assertEqual(
            '{"entries": []}',
            JSONSerializer().entries_to_string(entries)
        )

    def test_entries_to_string_serializes_correctly(self):
        entries = [
            Entry(data=dict(col1=1, col2='str1')),
            Entry(data=dict(col1=2, col2='str2')),
        ]

        self.assertEqual(
            '{"entries": [{"col1": 1, "col2": "str1"}, {"col1": 2, "col2": "str2"}]}',
            JSONSerializer().entries_to_string(entries)
        )

    def test_entries_to_string_deserializes_correctly(self):
        entries = [
            Entry(data=dict(col1=1, col2='str1')),
            Entry(data=dict(col1=2, col2='str2')),
        ]

        self.assertEqual(
            entries,
            JSONSerializer().entries_from_string(
                '{"entries": [{"col1": 1, "col2": "str1"}, {"col1": 2, "col2": "str2"}]}'
            )
        )

    def test_entries_from_string_raises_value_error_if_no_entries_key(self):
        with self.assertRaises(ValueError):
            JSONSerializer().entries_from_string(
                '{"some_wrong_key": [{"col1": 1, "col2": "str1"}]}'
            )

    def test_entries_from_string_raises_value_error_if_invalid_json(self):
        with self.assertRaises(ValueError):
            JSONSerializer().entries_from_string(
                '{"some_broken_json":'
            )
