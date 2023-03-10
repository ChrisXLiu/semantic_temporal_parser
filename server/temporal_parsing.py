from concurrent import futures
from sutime import SUTime
import grpc
import datetime

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

    def parse_iso_string(iso_string: str) -> datetime.time:
        return datetime.datetime.fromisoformat(iso_string)

    def format_time(time: datetime.time) -> datetime.time:
        return time.strftime('%Y-%m-%d %H:%M')

    def parse_reference_date(today: str | None) -> datetime.date | None:
        if today is None:
            return None
        try:
            return datetime.datetime.strptime(today, '%Y-%m-%d').date()
        except:
            return None

    def adjust_date(parsed_time: datetime.date,
                    reference_date: datetime.date) -> datetime.time:
        return reference_date - datetime.date.today() + parsed_time

    # Returns parsed time or None if unable to.
    def parse_internal(self, input: str) -> datetime.time | None:
        parsing_result = self.sutime.parse(input)
        if len(parsing_result) == 1 and parsing_result[0]["type"] == "TIME":
            return TemporalParsingService.parse_iso_string(parsing_result[0]["value"])
        else:
            return None

    def Parse(self, request, context):
        try:
            # First, try to parse the utterance
            parsed_time = self.parse_internal(request.utterance)
            if parsed_time is None:
                return TemporalParsingResponse(
                    status=TemporalParsingStatus.UNRECOGNIZED,
                    result="")

            # Second, try to adjust the date based on the reference date
            reference_date = TemporalParsingService.parse_reference_date(
                request.today)
            if reference_date is not None:
                parsed_time = TemporalParsingService.adjust_date(
                    parsed_time, reference_date)

            return TemporalParsingResponse(
                status=TemporalParsingStatus.SUCCEEDED,
                result=TemporalParsingService.format_time(parsed_time))
        except Exception as e:
            print(e)
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
