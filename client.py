import time
import grpc
import sys

import data_size as d
from protos import proto_pb2 as pb2
from protos import proto_pb2_grpc as pb2_grpc

CLIENT_ID = 1


class Client(object):

    def __init__(self, host_address):
        self.channel = grpc.insecure_channel(host_address)
        self.stub = pb2_grpc.AdaptiveStreamerStub(self.channel)


    def send_message(self, request_data):
        request = pb2.Request(client_id=CLIENT_ID,
                              request_data=request_data)
        return self.stub.ClientUnaryTransfer(request)


def stream_data():
    server_address = ""

    try:
        server_address = sys.argv[2]
    except IndexError:
        print("No proper address, taking localhost as server address")
        server_address = "localhost:8081"

    client = Client(host_address=server_address)

    start = time.time()

    DATASET = 'dataset/data.txt'
    with open(DATASET) as f:
        for piece in read_in_chunks(f):
            result = client.send_message(request_data=piece)

    end = time.time()
    print("Time taken for transfer = " , end-start)


def read_in_chunks(file_object):
    chunk_size = d.getChunkSize()
    print("ChunkSize: ", chunk_size)
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


if __name__ == '__main__':
    stream_data()
