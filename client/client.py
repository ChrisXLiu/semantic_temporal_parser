import os
import datetime

from flask import Flask, render_template, request
import grpc

from temporal_parsing_pb2 import TemporalParsingRequest, TemporalParsingStatus
from temporal_parsing_pb2_grpc import TemporalParsingStub

app = Flask(__name__)

temporal_parsing_host = os.getenv("TEMPORAL_PARSING_HOST", "localhost")
temporal_parsing_channel = grpc.insecure_channel(
    f"{temporal_parsing_host}:50051"
)
temporal_parsing_client = TemporalParsingStub(temporal_parsing_channel)


@app.route("/", methods=("GET", "POST"))
def render_test_page():
    if request.method == "POST" and request.form["utterance"] is not None:
        temporal_parsing_request = TemporalParsingRequest(
            today=request.form["today"] or datetime.date.today().strftime(
                "%Y-%m-%d"),
            utterance=request.form["utterance"]
        )
        temporal_parsing_response = temporal_parsing_client.Parse(
            temporal_parsing_request
        )
        match temporal_parsing_response.status:
            case TemporalParsingStatus.SUCCEEDED:
                result = temporal_parsing_response.result
            case TemporalParsingStatus.UNRECOGNIZED:
                result = "Sorry I didn't understand that."
            case _:
                result = "Server error."
        return render_template(
            "test.html",
            result=result,
        )
    else:
        return render_template(
            "test.html",
            result="",
        )
