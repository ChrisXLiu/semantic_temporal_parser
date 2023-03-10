import unittest
from spelling_correcter import SpellingCorrecter


class TestSpellingCorrecter(unittest.TestCase):

    def test_corrected_cases(self):
        self.assertEqual(
            SpellingCorrecter().correct('Suunday 2pm'),
            'Sunday 2 pm')
        self.assertEqual(
            SpellingCorrecter().correct('Nexx Monday at 2pm'),
            'Next Monday at 2 pm')
        self.assertEqual(
            SpellingCorrecter().correct('Teuesdey oif Nexx weak att 9 pm'),
            'Tuesday of Next week at 9 pm')

    def test_no_correction_needed(self):
        self.assertEqual(
            SpellingCorrecter().correct('Sunday 2 pm'),
            'Sunday 2 pm')
        self.assertEqual(
            SpellingCorrecter().correct('Next Monday at 2pm'),
            'Next Monday at 2 pm')
        self.assertEqual(
            SpellingCorrecter().correct('Tuesday of Next week at 9 pm'),
            'Tuesday of Next week at 9 pm')


if __name__ == '__main__':
    unittest.main()
