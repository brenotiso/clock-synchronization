from Clock import Clock
import socket
import threading
import time
import statistics


SLAVES = ['192.168.0.1']  # adicionar os IPs dos slaves
INITIAL_PORT = 7100

ports = []
times = []
mean_time = 0
local_clock = Clock()
sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_udp.settimeout(1)


class GetTime(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.i = index

    def run(self):
        try:
            request_time = time.time()
            sock_udp.sendto(ports[self.i].encode(), (SLAVES[self.i], 7000))
            response = sock_udp.recvfrom(1024).decode()
            response_time = time.time()
            times[self.i] = response + ((response_time - request_time) / 2)
        except socket.timeout:
            print('Time out {}'.format(SLAVES[self.i]))


class SendTime(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.i = index

    def run(self):
        adjust_time = mean_time - times[self.i]
        sock_udp.sendto(str(adjust_time).encode(), (SLAVES[self.i], 7000))

for index, slave in enumerate(SLAVES):
    port = str(INITIAL_PORT + index)
    ports.append(port)
    times.append(0)

threads = []
for index, slave in enumerate(SLAVES):
    threads.append(GetTime(index))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

local_time = local_clock.getClock()
times.append(local_time)
mean_time = round(statistics.mean(times))

# print('')
# print(local_time)
# print(times)
# print(mean_time)

for index, slave in enumerate(SLAVES):
    SendTime(index).start()

local_clock.adjustClock(mean_time - local_time)

# print('')
# print(local_time)
