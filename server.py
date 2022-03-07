import sys
import time
from concurrent import futures
from threading import Thread

import grpc

from protos import proto_pb2_grpc
from protos import proto_pb2

__all__ = 'Server'
SERVER_ID = 1


class Server(proto_pb2_grpc.AdaptiveStreamerServicer):

    def SimpleMethod(self, request, context):
        print("SimpleMethod called by client(%d) the message: %s" %
              (request.client_id, request.request_data))
        response = proto_pb2.Response(
            server_id=SERVER_ID,
            response_data="Python server SimpleMethod Ok!!!!")
        return response

    def ClientTransfer(self, request_iterator, context):
        start = time.time()
        print("ClientTransfer called by client...")
        for request in request_iterator:
            pass
            # print("recv from client(%d), message= %s" %
            #       (request.client_id, request.request_data))
        response = proto_pb2.Response(
            server_id=SERVER_ID,
            response_data="Python server ClientStreamingMethod ok")
        end = time.time()
        print("Time taken = ", end - start)
        return response


def main(server_address):
    server = grpc.server(futures.ThreadPoolExecutor())
    proto_pb2_grpc.add_AdaptiveStreamerServicer_to_server(Server(), server)
    server.add_insecure_port(server_address)
    print("------------------start Python GRPC server")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    try:
        server_address = sys.argv[2]
    except IndexError:
        print("No proper address, taking localhost as server address")
        server_address = "localhost:23333"
    main(server_address)
