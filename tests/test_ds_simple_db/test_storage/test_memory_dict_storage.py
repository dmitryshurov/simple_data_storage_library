from unittest import TestCase

from ds_simple_db.core.entry import Entry
from ds_simple_db.storage.memory_dict_storage import MemoryDictStorage


class TestMemoryDictStorage(TestCase):

    #
    # __init__()
    #

    def test_default_constructor_creates_empty_data(self):
        storage = MemoryDictStorage()

        self.assertDictEqual(dict(), storage._data)

    def test_constructor_sets_given_initial_data(self):
        storage = MemoryDictStorage(
            initial_data=dict(
                col1=[1, 2, 3],
                col2=['str1', 'str2', 'str3']
            )
        )

        self.assertDictEqual(
            dict(
                col1=[1, 2, 3],
                col2=['str1', 'str2', 'str3']
            ),
            storage._data
        )

    def test_constructor_raises_value_error_if_lengths_of_lists_are_not_equal(self):
        with self.assertRaises(ValueError):
            MemoryDictStorage(
                initial_data=dict(
                    col1=[1, 2, 3],
                    col2=['str1', 'str2']
                )
            )

    def test_constructor_raises_value_error_if_two_arguments_are_provided(self):
        with self.assertRaises(ValueError):
            MemoryDictStorage(
                initial_data=dict(),
                columns=list()
            )

    def test_constructor_raises_type_error_if_argument_is_not_dict(self):
        with self.assertRaises(TypeError):
            MemoryDictStorage(
                initial_data='not_a_dict'
            )

    def test_constructor_raises_type_error_if_dict_value_is_not_list(self):
        with self.assertRaises(TypeError):
            MemoryDictStorage(
                initial_data=dict(
                    col1=[],
                    col2=''
                )
            )

    def test_constructor_internal_data_is_deep_copied(self):
        initial_data = dict(
                col=['initial_data']
            )
        storage = MemoryDictStorage(initial_data=initial_data)
        initial_data['col'][0] = 'modified_data'

        self.assertDictEqual(
            dict(
                col=['initial_data']
            ),
            storage._data
        )

    def test_default_constructor_creates_correct_columns(self):
        storage = MemoryDictStorage(
            columns=['col1', 'col2']
        )

        self.assertDictEqual(
            dict(
                col1=[],
                col2=[]
            ),
            storage._data
        )

    #
    # columns()
    #

    def test_columns_method_is_correct(self):
        self.assertListEqual([], MemoryDictStorage().columns())
        self.assertListEqual(['col1', 'col2'], MemoryDictStorage(columns=['col1', 'col2']).columns())
        self.assertListEqual(['col1', 'col2'], MemoryDictStorage(initial_data=dict(col1=[], col2=[])).columns())

    #
    # insert()
    #

    def test_insert_affects_data(self):
        storage = MemoryDictStorage(columns=['name', 'address'])
        storage.insert(name='Dmitry', address='Moscow')

        self.assertDictEqual(
            dict(
                name=['Dmitry'],
                address=['Moscow']
            ),
            storage._data
        )

    def test_insert_returns_correct_entry(self):
        storage = MemoryDictStorage(columns=['name', 'address'])
        entry = storage.insert(name='Dmitry', address='Moscow')

        self.assertEqual(
            Entry(
                data=dict(
                    name='Dmitry',
                    address='Moscow'
                )
            ),
            entry
        )

    def test_insert_inserts_none_for_not_provided_columns(self):
        storage = MemoryDictStorage(columns=['name', 'address'])
        storage.insert(name='Dmitry')

        self.assertDictEqual(
            dict(
                name=['Dmitry'],
                address=[None]
            ),
            storage._data
        )

    def test_insert_raises_value_error_if_no_data_provided(self):
        storage = MemoryDictStorage(columns=['name', 'address'])

        with self.assertRaises(ValueError):
            storage.insert()

    def test_insert_raises_value_error_if_column_does_not_exist_in_storage(self):
        storage = MemoryDictStorage(columns=['name'])

        with self.assertRaises(ValueError):
            storage.insert(address='Moscow')

    #
    # all()
    #

    def test_all_returns_all_entries(self):
        storage = MemoryDictStorage(
            initial_data=dict(
                col1=[1, 2],
                col2=['str1', 'str2']
            )
        )

        self.assertListEqual(
            [
                Entry(data=dict(col1=1, col2='str1')),
                Entry(data=dict(col1=2, col2='str2')),
            ],
            storage.all_entries()
        )

    def test_all_returns_empty_list_if_no_entries(self):
        storage = MemoryDictStorage(
            initial_data=dict(
                col1=[],
                col2=[]
            )
        )

        self.assertListEqual([], storage.all_entries())

    def test_all_returns_empty_list_if_no_columns(self):
        storage = MemoryDictStorage(
            initial_data=dict()
        )

        self.assertListEqual([], storage.all_entries())

    #
    # filter()
    #

    def test_empty_filter_returns_no_entries(self):
        storage = MemoryDictStorage(
            initial_data=dict(
                col1=[1, 2],
                col2=['str1', 'str2']
            )
        )

        self.assertListEqual(
            [],
            storage.filter()
        )
