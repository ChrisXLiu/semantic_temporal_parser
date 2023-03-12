from concurrent import futures
from sutime import SUTime
import grpc
import datetime
import re

from temporal_parsing_pb2 import (
    TemporalParsingStatus,
    TemporalParsingRequest,
    TemporalParsingResponse,
)
import temporal_parsing_pb2_grpc


class TemporalParsingService(
    temporal_parsing_pb2_grpc.TemporalParsingServicer
):
    def __init__(self):
        self.sutime = SUTime(mark_time_ranges=False, include_range=True)

    def iso_string_to_time(iso_string: str) -> datetime.time:
        return datetime.datetime.fromisoformat(iso_string)

    def format_time(time: datetime.time) -> datetime.time:
        return time.strftime("%Y-%m-%d %H:%M")

    def is_implicit_next_week(utterance: str,
                              today_date: datetime.datetime,
                              parsed_time: datetime.time) -> bool:
        DAY_OF_WEEK_REGEX = r'\b(mon|monday|tue|tuesday|wed|wednesday|thu|thur|thursday|fri|friday|sat|saturday|sun|sunday)\b'
        return re.search(DAY_OF_WEEK_REGEX, utterance.lower()) is not None \
            and parsed_time < today_date < parsed_time + datetime.timedelta(days=7)

    # Returns parsed time or None if unable to.
    def parse_internal(self, input: str, reference_date: str) -> datetime.time | None:
        parsing_results = self.sutime.parse(input, reference_date)
        if TemporalParsingService.is_fully_parsed(input, parsing_results):
            return TemporalParsingService.iso_string_to_time(
                parsing_results[0]["value"])
        else:
            return None

    # Checks if the input string is parsed into a single recognized range,
    # and there are no important words lie outside of the recognized range.
    def is_fully_parsed(input: str, parsing_results):
        if len(parsing_results) != 1:
            return False
        parsing_result = parsing_results[0]
        type = parsing_result["type"]
        start = parsing_result["start"]
        end = parsing_result["end"]
        # Non-stop words include relative terms, digits, months, days of weeks.
        NON_STOP_WORDS_REGEX = r'[0-9]+|\b(last|next|upcoming|coming|week|month|jan|january|feb|feburary|mar|march|apr|april|may|jun|june|jul|july|aug|auguest|sep|sept|september|oct|october|nov|november|dec|december|mon|monday|tue|tuesday|wed|wednesday|thu|thur|thursday|fri|friday|sat|saturday|sun|sunday)\b'
        return type == "TIME" \
            and re.search(NON_STOP_WORDS_REGEX, input[0:start]) is None \
            and re.search(NON_STOP_WORDS_REGEX, input[end:-1]) is None

    def Parse(self, request, context):
        try:
            parsed_time = self.parse_internal(request.utterance, request.today)
            if parsed_time is None:
                return TemporalParsingResponse(
                    status=TemporalParsingStatus.UNRECOGNIZED,
                    result="")

            today_date = datetime.datetime.strptime(request.today, "%Y-%m-%d")
            if parsed_time < today_date:
                if TemporalParsingService.is_implicit_next_week(
                        request.utterance, today_date, parsed_time):
                    parsed_time += datetime.timedelta(days=7)
                else:
                    return TemporalParsingResponse(
                        status=TemporalParsingStatus.UNRECOGNIZED,
                        result="")

            return TemporalParsingResponse(
                status=TemporalParsingStatus.SUCCEEDED,
                result=TemporalParsingService.format_time(parsed_time))
        except ValueError as e:
            print(f'{e.__class__}:{e}')
            return TemporalParsingResponse(
                status=TemporalParsingStatus.UNRECOGNIZED,
                result="")
        except Exception as e:
            print(f'{e.__class__}:{e}')
            return TemporalParsingResponse(
                status=TemporalParsingStatus.SERVER_ERROR,
                result="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    temporal_parsing_pb2_grpc.add_TemporalParsingServicer_to_server(
        TemporalParsingService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
