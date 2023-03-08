from iparser import IParser
import datetime
import re


def weekday_to_numeric(weekday):
    if "mon" in weekday.lower():
        return 0
    if "tue" in weekday.lower():
        return 1
    if "wed" in weekday.lower():
        return 2
    if "thu" in weekday.lower():
        return 3
    if "fri" in weekday.lower():
        return 4
    if "sat" in weekday.lower():
        return 5
    if "sun" in weekday.lower():
        return 6
    raise


class RegexParser(IParser):
    def parse(self, today, utterance):
        pattern = "(sun(?:[.]|day)?|mon(?:[.]|day)?|tue(?:[.]|sday)?|wed(?:[.]|nesday)?|thu(?:[.]|rsday)?|fri(?:[.]|day)?|sat(?:[.]|urday)?)\s*(\d{1,2})([:]\d{1,2})?\s*(am|pm)?"
        matched = re.search(pattern, utterance.lower())
        if matched is None:
            return None
        num_matched_groups = len(matched.groups())
        if num_matched_groups < 2:
            return None
        day = weekday_to_numeric(matched.group(1))
        hour = int(matched.group(2))
        if matched.group(3) is not None:
            minute = int(matched.group(3).split(":")[-1])
        else:
            minute = 0
        am_pm = matched.group(4) or "am"
        today_date = datetime.datetime.strptime(today, "%Y-%m-%d")
        curr_day = today_date.weekday()
        if am_pm == "pm" and hour < 12:
            hour += 12
        # Assume people mean the upcoming X when they say X on day X
        days_delta = (day - curr_day + 7) % 7 if day != curr_day else 7
        return datetime.datetime.combine(
            today_date + datetime.timedelta(days=days_delta),
            datetime.time(hour, minute)).strftime("%Y-%m-%d %H:%M")
