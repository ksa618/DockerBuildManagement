import unittest

from ..ArgumentHandler import ArgumentHandler


class TestArgumentHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.argument_handler = ArgumentHandler()

    def test_help_argument_should_make_help_true(self):
        args = self.argument_handler.parse_arguments(['-help'])
        self.assertTrue(args.help)

    def test_no_help_argument_should_make_help_false(self):
        args = self.argument_handler.parse_arguments([])
        self.assertFalse(args.swarm)

    def test_selection_arguments(self):
        test_cases = (*self.create_selection_test_data_for('run'),
                      *self.create_selection_test_data_for('run', '-r'),
                      *self.create_selection_test_data_for('build'),
                      *self.create_selection_test_data_for('build', '-b'),
                      *self.create_selection_test_data_for('test'),
                      *self.create_selection_test_data_for('test', '-t'),
                      *self.create_selection_test_data_for('publish'),
                      *self.create_selection_test_data_for('publish', '-p'),
                      *self.create_selection_test_data_for('start'),
                      *self.create_selection_test_data_for('restart'),
                      *self.create_selection_test_data_for('stop'),
                      *self.create_selection_test_data_for('dump'),
                      *self.create_selection_test_data_for('swarm'),
                      *self.create_selection_test_data_for('swarm', '-s'))
        for test_case in test_cases:
            with self.subTest():
                args = self.argument_handler.parse_arguments(test_case['input_args'])
                self.assertEqual(test_case['expected'], getattr(args, test_case['attr']),
                                 f'Argument "{test_case["input_args"]}" failed. '
                                 f'Expected "{test_case["expected"]}", '
                                 f'got "{getattr(args, test_case["attr"])}"')

    def test_file_with_filename_should_set_file_to_filename(self):
        filename = 'file.yml'
        args = self.argument_handler.parse_arguments(['-f', filename])
        self.assertEqual(filename, args.config_file)

    def test_file_with_more_than_one_filename_should_set_file_to_first_filename(self):
        filename = 'file.yml'
        args = self.argument_handler.parse_arguments(['-f', filename, 'another file', 'yet another file'])
        self.assertEqual(filename, args.config_file)

    def test_file_with_no_filename_should_set_file_to_default(self):
        args = self.argument_handler.parse_arguments(['-f', '-build'])
        self.assertEqual('build-management.yml', args.config_file)

    def test_file_with_no_filename_and_trailing_argument_should_set_file_to_default(self):
        args = self.argument_handler.parse_arguments(['-f', '-build'])
        self.assertEqual('build-management.yml', args.config_file)

    def test_with_no_file_filename_should_set_file_to_default(self):
        args = self.argument_handler.parse_arguments(['-build'])
        self.assertEqual('build-management.yml', args.config_file)

    def test_all_arguments_should_be_equal_to_provided_arguments(self):
        expected = ['1', '2,', '3']
        args = self.argument_handler.parse_arguments(expected)
        self.assertEqual(expected, args.all_arguments)

    @staticmethod
    def create_selection_test_data_for(attribute_name, argument_name=None):
        selections = ['selection1', 'selection2']
        if not argument_name:
            argument_name = f'-{attribute_name}'
        return ({'input_args': [argument_name], 'attr': attribute_name, 'expected': True},
                {'input_args': [argument_name, *selections, '-help'], 'attr': attribute_name, 'expected': True},
                {'input_args': [argument_name, *selections, '-help'], 'attr': f'{attribute_name}_selections',
                 'expected': selections},
                {'input_args': ['-help'], 'attr': attribute_name, 'expected': False},
                {'input_args': ['-help'], 'attr': f'{attribute_name}_selections', 'expected': []})


if __name__ == '__main__':
    unittest.main()
