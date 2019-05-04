from argparse import Namespace


class ArgumentHandler:
    @staticmethod
    def parse_arguments(given_arguments):
        args = Namespace()
        args.all_arguments = given_arguments

        args.help = '-help' in given_arguments

        ArgumentHandler.parse_selection_arguments('run', given_arguments, args, '-r')
        ArgumentHandler.parse_selection_arguments('build', given_arguments, args, '-b')
        ArgumentHandler.parse_selection_arguments('test', given_arguments, args, '-t')
        ArgumentHandler.parse_selection_arguments('publish', given_arguments, args, '-p')
        ArgumentHandler.parse_selection_arguments('start', given_arguments, args)
        ArgumentHandler.parse_selection_arguments('restart', given_arguments, args)
        ArgumentHandler.parse_selection_arguments('stop', given_arguments, args)
        ArgumentHandler.parse_selection_arguments('dump', given_arguments, args)
        ArgumentHandler.parse_selection_arguments('swarm', given_arguments, args, '-s')

        file_arg = '-f'
        args.config_file = 'build-management.yml'
        if file_arg in given_arguments:
            filename_index = given_arguments.index(file_arg) + 1
            if not len(given_arguments) <= filename_index and not given_arguments[filename_index].startswith('-'):
                args.config_file = given_arguments[filename_index]

        return args

    @classmethod
    def parse_selection_arguments(cls, attribute_name, given_arguments, parsed_args, alias=None):
        argument = f'-{attribute_name}'
        if argument not in given_arguments:
            argument = alias
        if argument in given_arguments:
            setattr(parsed_args, attribute_name, True)
            setattr(parsed_args, f'{attribute_name}_selections',
                    ArgumentHandler.get_selections(argument, given_arguments))
        else:
            setattr(parsed_args, attribute_name, False)
            setattr(parsed_args, f'{attribute_name}_selections', [])

    @classmethod
    def get_selections(cls, argument, arguments):
        command_index = arguments.index(argument)
        remaining_args = arguments[command_index + 1:]
        result = []
        while remaining_args:
            current = remaining_args.pop(0)
            if current.startswith('-'):
                break
            result.append(current)
        return result
