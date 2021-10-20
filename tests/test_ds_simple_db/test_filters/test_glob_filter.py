from unittest import TestCase

from ds_simple_db.core.entry import Entry
from ds_simple_db.filters.glob_filter import GlobFilter


class TestGlobFilter(TestCase):
    def test_raises_type_error_if_argument_type_not_str(self):
        with self.assertRaises(TypeError):
            GlobFilter(1)

    def test_construct_and_satisfies(self):
        entry = Entry(data=dict(name='Dmitry', address='Moscow'))

        self.assertTrue(GlobFilter('name=*').satisfies(entry))
        self.assertTrue(GlobFilter('name=Dm*').satisfies(entry))
        self.assertTrue(GlobFilter('name=Dmitry').satisfies(entry))
        self.assertFalse(GlobFilter('name=Se*').satisfies(entry))

    def test_raises_value_error_if_field_does_not_exist_in_entry(self):
        entry = Entry(data=dict(name='Dmitry', address='Moscow'))

        with self.assertRaises(ValueError):
            self.assertTrue(GlobFilter('phone_number=000').satisfies(entry))
