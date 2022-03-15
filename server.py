import sys
from concurrent import futures

import config
import grpc

from protos import proto_pb2_grpc as pb2_grpc
from protos import proto_pb2 as pb2

SERVER_ID = 1


class Server(pb2_grpc.AdaptiveStreamerServicer):

    def __init__(self):
        pass

    def ClientUnaryTransfer(self, request, context):
        response = pb2.Response(
            server_id=SERVER_ID,
            response_data="Received by server",
            received=(request.hash_value == hash(request.request_data)))
        return response


def serve():
    server_address = "0.0.0.0:8000"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         options=[
                             ('grpc.max_send_message_length', config.MAX_PACKET_LENGTH),
                             ('grpc.max_receive_message_length', config.MAX_PACKET_LENGTH),
                         ])
    pb2_grpc.add_AdaptiveStreamerServicer_to_server(Server(), server)
    server.add_insecure_port(server_address)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
