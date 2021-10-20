import argparse
import os

from . import PersonalDataCommand
from ..display import DisplayFactory


class InsertCmd(PersonalDataCommand):
    name = 'insert'

    def exec(self, command_args):
        parser = argparse.ArgumentParser(self.name)
        parser.add_argument('--path', type=str, required=True, help='Path to a serialized database')
        parser.add_argument('--values', type=str, required=True, help='Comma-separated values to insert')
        args = parser.parse_args(command_args)

        self.insert(args.path, args.values.split(','))

    def insert(self, db_path, values):
        if len(values) != len(self.DB_COLUMNS):
            raise ValueError('Please specify exactly 3 columns')

        storage = self.create_storage()

        if os.path.exists(db_path):
            storage.load_from_file(db_path)

        dict_to_insert = dict(zip(self.DB_COLUMNS, values))
        storage.insert(**dict_to_insert)

        storage.save_to_file(db_path)

        DisplayFactory.create('table').display(storage.all_entries())
