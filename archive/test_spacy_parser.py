import unittest

import unittest
from unittest.mock import Mock
from spacy_parser import SpacyParser


class TestSpacyParser(unittest.TestCase):

    def test_entities(self):
        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'tomorrow at 2pm'),
            'tomorrow,2pm')

        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'tomorrow at 11am'),
            'tomorrow,11am')

        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'tomorrow at 11 am'),
            'tomorrow,11 am')

        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'This coming Tuesday at 9pm'),
            'This coming Tuesday,9pm')

        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'Next Monday at 10'),
            'Next Monday')

        # WHY 2:30pm is not recognized?
        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'Tomorrow at 2:30pm'),
            'Tomorrow')

        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'Tomorrow at 2:30 pm'),
            'Tomorrow,2:30 pm')

        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', 'Next Monday at 10:30'),
            'Next Monday,10:30')

        # This is odd
        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', '14:30 the Monday after next week'),
            '14:30 the Monday,next week')

        self.assertEqual(
            SpacyParser().parse(
                '2023-03-08', '14:30 on Monday after next week'),
            '14:30,Monday,next week')
