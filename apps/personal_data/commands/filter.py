import argparse

from . import PersonalDataCommand

from ds_simple_db.filters.glob_filter import GlobFilter
from ..display import DisplayFactory


class FilterCmd(PersonalDataCommand):
    name = 'filter'

    def exec(self, command_args):
        parser = argparse.ArgumentParser(self.name)
        parser.add_argument('--path', type=str, required=True, help='Path to a serialized database')
        parser.add_argument('--glob', type=str, required=True, help='A glob pattern to apply as a filter')
        parser.add_argument('--display', type=str, default='table', help='Display format (table/html). Default is table')
        args = parser.parse_args(command_args)

        self.filter(args.path, args.glob, args.display)

    def filter(self, db_path, glob_pattern, display_format):
        storage = self.create_storage()
        storage.load_from_file(db_path)

        filtered_entries = storage.filter(GlobFilter(glob_pattern))

        if len(filtered_entries) == 0:
            print("\nINFO: No entries satisfying the given filter found")
        else:
            DisplayFactory.create(display_format).display(filtered_entries)
