# This is a sample Python script.
import pyshark
import psutil
import time

bandwidths = []
n = 0
average = 0.0


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


# Press the green button in the gutter to run the script.

while True:
    print(get_bandwidth())
