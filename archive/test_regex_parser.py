import unittest
from regex_parser import RegexParser


class TestRegexParser(unittest.TestCase):

    def test_full_day_no_minute(self):
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Sunday 2pm'),
            '2023-03-12 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Monday 2pm'),
            '2023-03-13 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Tuesday 2pm'),
            '2023-03-14 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Wednesday 2pm'),
            '2023-03-15 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Thursday 2pm'),
            '2023-03-09 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Friday 2pm'),
            '2023-03-10 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Saturday 2pm'),
            '2023-03-11 14:00')

    def test_short_day_no_minute(self):
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Sun. 2pm'),
            '2023-03-12 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Mon 2pm'),
            '2023-03-13 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Tue. 2pm'),
            '2023-03-14 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Wed 2pm'),
            '2023-03-15 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Thu. 2pm'),
            '2023-03-09 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Fri 2pm'),
            '2023-03-10 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Sat. 2pm'),
            '2023-03-11 14:00')

    def test_lower_case_no_minute(self):
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'sunday 2pm'),
            '2023-03-12 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'mon. 2pm'),
            '2023-03-13 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'tue 2pm'),
            '2023-03-14 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'wednesday 2pm'),
            '2023-03-15 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'thu 2pm'),
            '2023-03-09 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'fri. 2pm'),
            '2023-03-10 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'sat 2pm'),
            '2023-03-11 14:00')

    def test_with_minute(self):
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'sun 2:30pm'),
            '2023-03-12 14:30')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Mon 2:15am'),
            '2023-03-13 02:15')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Tue. 2:00 pm'),
            '2023-03-14 14:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Wednesday 2:45am'),
            '2023-03-15 02:45')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'thu 2:35 pm'),
            '2023-03-09 14:35')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Fri 2:10 am'),
            '2023-03-10 02:10')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Sat 2:05pm'),
            '2023-03-11 14:05')

    def test_no_am_pm(self):
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'sun 14:30'),
            '2023-03-12 14:30')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Mon 2:15'),
            '2023-03-13 02:15')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Tue. 15:00'),
            '2023-03-14 15:00')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Wednesday 2:45'),
            '2023-03-15 02:45')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'thu 18:35'),
            '2023-03-09 18:35')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Fri 20:10'),
            '2023-03-10 20:10')
        self.assertEqual(
            RegexParser().parse('2023-03-08', 'Sat 22:05'),
            '2023-03-11 22:05')

    def test_unsupported_cases(self):
        self.assertIsNone(
            RegexParser().parse('2023-03-08', 'Upcoming Tuesday at 2pm'))
        self.assertIsNone(
            RegexParser().parse('2023-03-08', 'Today at 2pm'))
        self.assertIsNone(
            RegexParser().parse('2023-03-08', '3pm tomorrow'))
        self.assertIsNone(
            RegexParser().parse('2023-03-08', 'Next Tuesday at 2pm'))
        self.assertIsNone(
            RegexParser().parse('2023-03-08', 'Tuesday of next week at 2pm'))
        self.assertIsNone(
            RegexParser().parse('2023-03-08', 'Frody at non'))


if __name__ == '__main__':
    unittest.main()
