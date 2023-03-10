import unittest
from unittest.mock import Mock
from first_success_strategy import FirstSuccessStrategy


class TestFirstSuccessStrategy(unittest.TestCase):

    def test_no_parsers_return_none(self):
        parser_1 = Mock()
        parser_1.parse.return_value = "Result 1"
        parser_2 = Mock()
        parser_2.parse.return_value = "Result 2"
        self.assertEqual(
            FirstSuccessStrategy().run(
                '2023-03-08', 'Suunday 2pm', [parser_1, parser_2]),
            'Result 1')
        self.assertEqual(
            FirstSuccessStrategy().run(
                '2023-03-08', 'Suunday 2pm', [parser_2, parser_1]),
            'Result 2')

    def test_some_parsers_return_none(self):
        parser_1 = Mock()
        parser_1.parse.return_value = None
        parser_2 = Mock()
        parser_2.parse.return_value = "Result 2"
        self.assertEqual(
            FirstSuccessStrategy().run(
                '2023-03-08', 'Suunday 2pm', [parser_1, parser_2]),
            'Result 2')
        self.assertEqual(
            FirstSuccessStrategy().run(
                '2023-03-08', 'Suunday 2pm', [parser_2, parser_1]),
            'Result 2')


if __name__ == '__main__':
    unittest.main()
