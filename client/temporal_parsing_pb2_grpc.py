# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import temporal_parsing_pb2 as temporal__parsing__pb2


class TemporalParsingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Parse = channel.unary_unary(
                '/TemporalParsing/Parse',
                request_serializer=temporal__parsing__pb2.TemporalParsingRequest.SerializeToString,
                response_deserializer=temporal__parsing__pb2.TemporalParsingResponse.FromString,
                )


class TemporalParsingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Parse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TemporalParsingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Parse': grpc.unary_unary_rpc_method_handler(
                    servicer.Parse,
                    request_deserializer=temporal__parsing__pb2.TemporalParsingRequest.FromString,
                    response_serializer=temporal__parsing__pb2.TemporalParsingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TemporalParsing', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TemporalParsing(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Parse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TemporalParsing/Parse',
            temporal__parsing__pb2.TemporalParsingRequest.SerializeToString,
            temporal__parsing__pb2.TemporalParsingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
