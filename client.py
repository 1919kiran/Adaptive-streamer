import time
import grpc
import sys
import psutil
import threading
from protos import proto_pb2 as pb2
from protos import proto_pb2_grpc as pb2_grpc
import config
import hashlib

CLIENT_ID = 1
average = 0.0
n = 0
bandwidths = []
packet_loss = []


class Client(object):

    def __init__(self, host_address, max_packet_length=config.MAX_PACKET_LENGTH):
        self.channel = grpc.insecure_channel(host_address,
                                             options=[
                                                 ('grpc.max_send_message_length', max_packet_length),
                                                 ('grpc.max_receive_message_length', max_packet_length),
                                             ])
        self.stub = pb2_grpc.AdaptiveStreamerStub(self.channel)

    chunkSize = config.PACKET_SIZE

    def send_message(self, request_data, hash_value):
        request = pb2.Request(client_id=CLIENT_ID,
                              request_data=request_data,
                              hash_value=hash_value)
        return self.stub.ClientUnaryTransfer(request)


def getChunkSize():
    return Client.chunkSize


def stream_data():
    client = Client(host_address=config.SERVER)
    start = time.time()
    latency = []
    with open(config.DATASET) as f:
        for piece in read_in_chunks(f):
            chunk_start = time.time()
            result = client.send_message(request_data=piece, hash_value=str(hashlib.md5(piece.encode()).hexdigest()))
            packet_loss.append(result.received)
            latency.append(time.time() - chunk_start)

    end = time.time()
    print("Time taken for transfer = ", end - start)
    print(max(latency))
    print(packet_loss)
    exit(0)


def read_in_chunks(file_object):
    while True:
        print("ChunkSize: ", Client.chunkSize)
        # print("Chunk Size: ", Client.chunkSize)
        data = file_object.read(Client.chunkSize)
        if not data:
            break
        yield data


# Function to get current traffic on the channel
def get_bandwidth(bandwidths):
    global n, average
    # Get net in/out
    net1_out = psutil.net_io_counters().bytes_sent
    net1_in = psutil.net_io_counters().bytes_recv

    time.sleep(1)

    # Get new net in/out
    net2_out = psutil.net_io_counters().bytes_sent
    net2_in = psutil.net_io_counters().bytes_recv

    # Compare and get current speed
    if net1_in > net2_in:
        current_in = 0
    else:
        current_in = net2_in - net1_in

    if net1_out > net2_out:
        current_out = 0
    else:
        current_out = net2_out - net1_out

    bandwidths.append(current_out)
    if n < 10:
        prev = 0
        n += 1
    else:
        prev = bandwidths.pop(0)
    average = ((average * 10) - prev + current_out) / 10

    network = {"traffic_in": current_in, "traffic_out": current_out, "average": average}
    return network


def average_bandwidth():
    prev = None
    while True:
        traffic_values = get_bandwidth([])
        print(traffic_values)
        if not prev:
            prev = traffic_values['average']
            continue

        # Below if...else conditions are for variance detection to resize packet size
        elif traffic_values['average'] - prev > 2000:
            Client.chunkSize = int(traffic_values['traffic_out'] * 0.5)
        elif prev - traffic_values['average'] > 2000:
            Client.chunkSize = int(traffic_values['traffic_out'] * 0.5)

        # setting prev value to current value to detect variance in next loop
        prev = traffic_values['average']
        # print("Chunk-Size: ", Client.chunkSize)


if __name__ == '__main__':
    #threading.Thread(target=average_bandwidth).start()
    threading.Thread(target=stream_data).start()
