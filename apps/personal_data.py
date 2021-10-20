import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')

from ds_command.command_runner import CommandRunner

from personal_data.commands.convert import ConvertCmd
from personal_data.commands.display import DisplayCmd
from personal_data.commands.filter import FilterCmd
from personal_data.commands.insert import InsertCmd


class MainCommandRunner(CommandRunner):
    commands = [InsertCmd, DisplayCmd, ConvertCmd, FilterCmd]


def parse_args():
    parser = argparse.ArgumentParser('Simple data storage CLI')
    parser.add_argument('command', type=str, help='A command to run (insert, display, filter, convert)')

    return parser.parse_known_args()


def main():
    main_args, command_args = parse_args()
    MainCommandRunner().run(main_args.command, command_args)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
