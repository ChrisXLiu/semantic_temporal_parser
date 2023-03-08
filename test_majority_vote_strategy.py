import unittest
from unittest.mock import Mock
from majority_vote_strategy import MajorityVoteStrategy


class TestMajorityVoteStrategy(unittest.TestCase):

    def test_has_majority_vote(self):
        parser_1 = Mock()
        parser_1.parse.return_value = "Result 1"
        parser_2 = Mock()
        parser_2.parse.return_value = "Result 2"
        parser_3 = Mock()
        parser_3.parse.return_value = "Result 1"
        self.assertEqual(
            MajorityVoteStrategy().run(
                '2023-03-08', 'Suunday 2pm', [parser_1, parser_2, parser_3]),
            'Result 1')
        self.assertEqual(
            MajorityVoteStrategy().run(
                '2023-03-08', 'Suunday 2pm', [parser_2, parser_1, parser_3]),
            'Result 1')

    def test_has_majority_vote_modulo_nulls(self):
        parser_1 = Mock()
        parser_1.parse.return_value = "Result 1"
        parser_2 = Mock()
        parser_2.parse.return_value = "Result 2"
        parser_3 = Mock()
        parser_3.parse.return_value = "Result 1"
        parser_4 = Mock()
        parser_4.parse.return_value = None
        parser_5 = Mock()
        parser_5.parse.return_value = None
        self.assertEqual(
            MajorityVoteStrategy().run(
                '2023-03-08', 'Suunday 2pm',
                [parser_1, parser_2, parser_3, parser_4, parser_5]),
            'Result 1')
        self.assertEqual(
            MajorityVoteStrategy().run(
                '2023-03-08', 'Suunday 2pm',
                [parser_5, parser_4, parser_3, parser_2, parser_1]),
            'Result 1')

    def test_no_majority_vote(self):
        parser_1 = Mock()
        parser_1.parse.return_value = "Result 1"
        parser_2 = Mock()
        parser_2.parse.return_value = "Result 2"
        parser_3 = Mock()
        parser_3.parse.return_value = "Result 1"
        parser_4 = Mock()
        parser_4.parse.return_value = "Result 3"
        parser_5 = Mock()
        parser_5.parse.return_value = "Result 3"
        self.assertIsNone(
            MajorityVoteStrategy().run(
                '2023-03-08', 'Suunday 2pm',
                [parser_1, parser_2, parser_3, parser_4, parser_5]))


if __name__ == '__main__':
    unittest.main()
