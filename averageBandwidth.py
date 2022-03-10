# This is a sample Python script.
import pyshark
import psutil
import time

import data_size
import data_size as d

bandwidths = []
n = 0
average = 0.0

# Function to get current traffic on the channel
def get_bandwidth():
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


# Below main function will detect current traffic every 10s on channel to decide upon next packet size to be sent.
prev = None
while True:
    traffic_values = get_bandwidth()
    print(traffic_values)
    if not prev:
        prev = traffic_values['average']
        continue

    # Below if...else conditions are for variance detection to resize packet size
    elif traffic_values['average']-prev > 2000:
        d.setChunkSize((traffic_values['traffic_out']//100)*100)
    elif prev - traffic_values['average'] > 2000:
        d.setChunkSize((traffic_values['traffic_out']//100)*100)

    # setting prev value to current value to detect variance in next loop
    prev = traffic_values['average']
    print("Chunk Size: ", d.getChunkSize())
