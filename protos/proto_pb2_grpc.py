# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import proto_pb2 as protos_dot_proto__pb2


class AdaptiveStreamerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ClientTransfer = channel.stream_unary(
                '/AdaptiveStreamer/ClientTransfer',
                request_serializer=protos_dot_proto__pb2.Request.SerializeToString,
                response_deserializer=protos_dot_proto__pb2.Response.FromString,
                )


class AdaptiveStreamerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ClientTransfer(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdaptiveStreamerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ClientTransfer': grpc.stream_unary_rpc_method_handler(
                    servicer.ClientTransfer,
                    request_deserializer=protos_dot_proto__pb2.Request.FromString,
                    response_serializer=protos_dot_proto__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AdaptiveStreamer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AdaptiveStreamer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ClientTransfer(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/AdaptiveStreamer/ClientTransfer',
            protos_dot_proto__pb2.Request.SerializeToString,
            protos_dot_proto__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
