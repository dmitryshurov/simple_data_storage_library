import argparse

from . import PersonalDataCommand
from ..display import DisplayFactory


class DisplayCmd(PersonalDataCommand):
    name = 'display'

    def exec(self, command_args):
        parser = argparse.ArgumentParser(self.name)
        parser.add_argument('--path', type=str, required=True, help='Path to a serialized database')
        parser.add_argument('--format', type=str, default='table', help='Display format (table/html). Default is table')
        args = parser.parse_args(command_args)

        self.display(args.path, args.format)

    def display(self, db_path, display_format):
        storage = self.create_storage()
        storage.load_from_file(db_path)

        DisplayFactory.create(display_format).display(storage.all_entries())
