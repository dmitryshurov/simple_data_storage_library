from unittest import TestCase
from ds_simple_db.core.entry import Entry


class TestEntry(TestCase):
    def test_construct_empty(self):
        entry = Entry()

        self.assertDictEqual(
            dict(),
            entry._data
        )

    def test_construct_raises_value_error_if_data_is_not_dict(self):
        with self.assertRaises(TypeError):
            Entry(data='str')

    def test_constructor_sets_given_initial_data(self):
        entry = Entry(
            data=dict(
                col1=1,
                col2='str1',
            )
        )

        self.assertDictEqual(
            dict(
                col1=1,
                col2='str1',
            ),
            entry._data
        )

    def test_constructor_internal_data_is_deep_copied(self):
        data = dict(
            col1=1,
            col2='str1',
        )

        entry = Entry(data)

        data['col1'] = 2

        self.assertDictEqual(
            dict(
                col1=1,
                col2='str1',
            ),
            entry._data
        )

    def test_columns(self):
        entry = Entry(data=dict(col1=1, col2='str1'))

        self.assertListEqual(
            ['col1', 'col2'],
            entry.fields()
        )

    def test_getattr_returns_correct_values(self):
        entry = Entry(data=dict(col1=1, col2='str1'))

        self.assertEqual(1, entry.col1)
        self.assertEqual(1, entry['col1'])

        self.assertEqual('str1', entry.col2)
        self.assertEqual('str1', entry['col2'])

    def test_getattr_raises_value_error_if_non_existing_column_given(self):
        entry = Entry(data=dict(col1=1, col2='str1'))

        with self.assertRaises(ValueError):
            entry.non_existing_column

        with self.assertRaises(ValueError):
            entry['non_existing_column']

    def test_equal(self):
        entry1 = Entry(data=dict(col1=1, col2='str1'))
        entry2 = Entry(data=dict(col1=1, col2='str1'))

        self.assertEqual(entry1, entry2)

    def test_not_equal(self):
        entry1 = Entry(data=dict(col1=1, col2='str1'))
        entry2 = Entry(data=dict(col1=1, col2='str2'))

        self.assertNotEqual(entry1, entry2)
