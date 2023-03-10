import unittest
from gpt_parser import GptParser


class TestGptParser(unittest.TestCase):

    def test_precise_cases(self):
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Sunday 2pm'),
            '2023-03-12 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Monday 2pm'),
            '2023-03-13 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Tuesday 2pm'),
            '2023-03-14 14:00')
        # This case shows a suboptinal result.
        # Note that 2023-03-08 is a Wednesday.
        # In reality, people would have said Next Wed or The upcoming Wed.
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Wednesday 2pm'),
            '2023-03-08 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Thursday 2pm'),
            '2023-03-09 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Friday 2pm'),
            '2023-03-10 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Saturday 2pm'),
            '2023-03-11 14:00')

    def test_semantic_cases(self):
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Upcoming Tuesday at 2pm'),
            '2023-03-14 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Today at 2pm'),
            '2023-03-08 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', '3pm tomorrow'),
            '2023-03-09 15:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Next Tuesday at 2pm'),
            '2023-03-14 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Tuesday of next week at 2pm'),
            '2023-03-14 14:00')
        self.assertEqual(
            GptParser().parse('2023-03-08', 'Teuesdey oif Nexx weak att 9 pm'),
            '2023-03-14 21:00')


if __name__ == '__main__':
    unittest.main()
