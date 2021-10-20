class CommandRunner:
    commands = []

    def run(self, command, command_args):
        """
        Run the command with given args if the command is registered

        :param command: a name of the command
        :param command_args: command arguments
        """
        commands_dict = self.commands_dict()

        if command in commands_dict:
            commands_dict[command]().run(command_args)
        else:
            self.command_not_found(command)

    def commands_dict(self):
        return {command.name: command for command in self.commands}

    def commands_names_list(self):
        return [command.name for command in self.commands]

    def command_not_found(self, command):
        print(f'Command `{command}` not found')
        print(f'Available commands: ', self.commands_names_list())
