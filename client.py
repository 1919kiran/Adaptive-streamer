import time
import grpc
import sys

from protos import proto_pb2
from protos import proto_pb2_grpc

CLIENT_ID = 1


def client_streaming_method(stub):
    print("--------------Call ClientStreamingMethod Begin--------------")

    CHUNK_SIZE = 1024
    DATASET = 'dataset/data.txt'

    # create a generator
    def request_messages():
        DATASET = 'dataset/data.txt'
        with open(DATASET) as f:
            i = 1
            for piece in read_in_chunks(f):
                # print('processing chunk : ', i)
                # print(piece)
                i += 1
                request = proto_pb2.Request(
                    client_id=CLIENT_ID,
                    request_data=piece)
                yield request

    def read_in_chunks(file_object, chunk_size=4096):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    response = stub.ClientTransfer(request_messages())
    print("resp from server(%d), the message=%s" %
          (response.server_id, response.response_data))
    print("--------------Call ClientStreamingMethod Over---------------")


def main(server_address):
    with grpc.insecure_channel(server_address) as channel:
        stub = proto_pb2_grpc.AdaptiveStreamerStub(channel)
        client_streaming_method(stub)


if __name__ == '__main__':
    try:
        server_address = sys.argv[2]
    except IndexError:
        print("No proper address, taking localhost as server address")
        server_address = "localhost:23333"
    main(server_address)
