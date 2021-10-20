class Command:
    """
    The string name of a command that is used as the first command line argument.

    Must be defined in a subclass
    """
    name = None

    def run(self, command_args):
        """
        The wrapper code
        :param command_args: Command line args to pass to the command
        """
        print(f'Running command `{self.name}` with args: {command_args}')
        self.exec(command_args)

    def exec(self, command_args):
        """
        The main command code. This should be defined in a subclass

        :param command_args: Command line args to pass to the command
        """
        pass
