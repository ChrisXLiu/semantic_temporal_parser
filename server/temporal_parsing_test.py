from temporal_parsing import TemporalParsingService

from temporal_parsing_pb2 import TemporalParsingStatus, TemporalParsingRequest

import unittest


class TestParsingService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._service = TemporalParsingService()

    ########################################
    # Group 1: Relative dates
    def test_today_explicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="today at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-24 11:00")

    def test_today_implicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-24 11:00")

    def test_tomorrow(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="tomorrow at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 11:00")

    def test_day_of_week_same_week(self):
        # Note 2023-02-24 is a Friday
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Saturday at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 11:00")

    def test_day_of_week_next_week_implicit(self):
        # Note 2023-02-24 is a Friday
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Monday at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-27 11:00")

    def test_day_of_week_next_week_explicit(self):
        # Note 2023-02-24 is a Friday
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Next Tuesday at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-28 11:00")

    def test_day_of_week_coming_week_explicit(self):
        # Note 2023-02-24 is a Friday
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="The coming Wednesday at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-03-01 11:00")

    # TODO: Do we need to handle "The upcoming"?
    def test_day_of_week_upcoming_week_explicit(self):
        # Note 2023-02-24 is a Friday
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="The upcoming Wednesday at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    # TODO: Do we need to handle "on the {}th of this month"?
    def test_date_same_month(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On the 26th of this month at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    # TODO: Do we need to handle "on the {}th of next month"?
    def test_date_next_month_explicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On the 3rd of the next month at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    # TODO: Do we need to handle this implicit case?
    def test_date_next_month_implicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On the 3rd at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    # TODO: Do we need to handle "In x days"
    def test_date_in_x_days(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="In 2 days at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    # TODO: Do we need to handle "In x days"
    def test_date_in_x_days_cross_month_boundary(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="In 7 days at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    ########################################
    # Group 2: Semi-absolute dates (assuming within a year)

    def test_specific_date(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On March 3rd at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-03-03 11:00")

    def test_specific_date_abundant_info(self):
        request = TemporalParsingRequest(
            today="2023-03-12", utterance="Tuesday March 14th 3pm"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-03-14 15:00")

    def test_specific_date_abbr_month(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On Mar 3rd at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-03-03 11:00")

    def test_specific_date_abbr_month_abbr_day(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On Mar 3 at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-03-03 11:00")

    def test_specific_date_cross_year_boundary_explicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On Jan 3rd next year at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2024-01-03 11:00")

    # TODO: Do we need to handle implict next year
    def test_specific_date_cross_year_boundary_implict(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On Jan 3rd at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_feb_29_leap_year(self):
        request = TemporalParsingRequest(
            today="2000-01-01", utterance="On Feb 29th at 11 am"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2000-02-29 11:00")

    ########################################
    # Group 3: Invalid dates

    def test_invalid_feb_29_non_leap_year(self):
        request = TemporalParsingRequest(
            today="2023-01-01", utterance="On Feb 29th at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_invalid_feb_30(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On Feb 30th at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_invalid_31(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On Apr 31st at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_invalid_32(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="On March 32nd at 11 am"
        )
        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    ########################################
    # Group 4: Time expressions

    def test_hour_only_am(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 11 am"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 11:00")

    def test_hour_minute_am(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 11:25 am"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 11:25")

    def test_hour_only_am_no_space(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 11am"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 11:00")

    def test_hour_minute_am_no_space(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 11:25am"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 11:25")

    def test_hour_only_pm(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 2 pm"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 14:00")

    def test_hour_minute_pm(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 2:25 pm"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 14:25")

    def test_hour_only_pm_no_space(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 2pm"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 14:00")

    def test_hour_minute_pm_no_space(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 2:25pm"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 14:25")

    # TODO: Do we need to handle such implicit cases?
    def test_hour_only_am_implicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 11"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_hour_minute_am_implicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 11:30"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 11:30")

    # TODO: Do we need to handle such implicit cases?
    def test_hour_only_pm_implicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 15"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_hour_minute_pm_implicit(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 15:30"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 15:30")

    # TODO: Do we need to handle this malformed format?
    def test_single_digit_minute(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 15:5"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_hour_padded_with_zero(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 02:30pm"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.SUCCEEDED)
        self.assertEqual(response.result, "2023-02-25 14:30")

    ########################################
    # Group 5: Invalid times

    def test_out_of_bound_hour(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 25:00"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)

    def test_out_of_bound_minute(self):
        request = TemporalParsingRequest(
            today="2023-02-24", utterance="Tomorrow at 12:70"
        )

        response = __class__._service.Parse(request, None)
        self.assertEqual(response.status, TemporalParsingStatus.UNRECOGNIZED)
