import argparse

from . import PersonalDataCommand


class ConvertCmd(PersonalDataCommand):
    name = 'convert'

    def exec(self, command_args):
        parser = argparse.ArgumentParser(self.name)
        parser.add_argument('--path', type=str, required=True, help='Path to a serialized database')
        parser.add_argument('--converted_path', type=str, required=True, help='Path to save a converted database')
        args = parser.parse_args(command_args)

        self.convert(args.path, args.converted_path)

    def convert(self, db_path, converted_db_path):
        storage = self.create_storage()
        storage.load_from_file(db_path)

        storage.save_to_file(converted_db_path)

        print("Conversion finished")
