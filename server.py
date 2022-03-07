import sys
import time
from concurrent import futures
from threading import Thread

import grpc

from protos import proto_pb2_grpc as pb2_grpc
from protos import proto_pb2 as pb2

SERVER_ID = 1


class Server(pb2_grpc.AdaptiveStreamerServicer):

    def __init__(self):
        pass

    def ClientUnaryTransfer(self, request, context):
        # print("SimpleMethod called by client(%d) the message: %s" %
        #       (request.client_id, request.request_data))
        response = pb2.Response(
            server_id=SERVER_ID,
            response_data="Python server SimpleMethod Ok!!!!")
        return response


def serve():
    try:
        server_address = sys.argv[2]
    except IndexError:
        print("No proper address, taking localhost as server address")
        server_address = "localhost:50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AdaptiveStreamerServicer_to_server(Server(), server)
    server.add_insecure_port(server_address)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
