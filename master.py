from Clock import Clock
import socket
import threading
import time
import statistics


SLAVES = ['192.168.103.16', '192.168.103.18']
SLAVE_PORT = 7101
INITIAL_PORT = 7101

local_clock = Clock()
sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Obtem o tempo dos slaves para realizar a média
class GetTime(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.i = index

    def run(self):
        try:
            request_time = time.time()
            sock_udp.sendto(str(ports[self.i]).encode(), (SLAVES[self.i], SLAVE_PORT))

            sock_udp_response = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock_udp_response.bind(('', ports[self.i]))

            response = sock_udp_response.recvfrom(1024)
            response_time = time.time()
            # O tempo é armazenado já com a compensação do atraso
            times[self.i] = int(response[0].decode()) + (int(response_time - request_time) // 2)

            sockets_response.append(sock_udp_response)
        except socket.timeout:
            print('Time out {}'.format(SLAVES[self.i]))


# Obtem o tempo dos slaves
class GetResults(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.i = index

    def run(self):
        result = sockets_response[self.i].recvfrom(1024)
        results.append(result[0].decode())


def main():
    while True:
        sockets_response = []
        ports = []
        times = []
        results = []

        # Defini as portas que serão utilizadas
        for index, slave in enumerate(SLAVES):
            port = INITIAL_PORT + index
            ports.append(port)
            times.append(0)

        # Coleta dos tempo dos slaves
        threads = []
        for index, slave in enumerate(SLAVES):
            threads.append(GetTime(index))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Adiconando o tempo do master para calcular a média
        local_time = local_clock.getClock()
        times.append(local_time)
        mean_time = round(statistics.mean(times))

        print('')
        print('Tempo local: ', local_time)
        print('Tempo dos slaves: ', times)
        print('Tempo  médio: ', mean_time)

        # Enviando para cada slave o quanto o tempo dele deve ser ajustado
        for index, slave in enumerate(SLAVES):
            adjust_time = mean_time - times[index]
            sock_udp.sendto(str(adjust_time).encode(), (SLAVES[index], SLAVE_PORT))

        local_clock.adjustClock(mean_time - local_time)
        local_date = local_clock.getDate()

        # Coleta dos resultados
        threads = []
        for index, slave in enumerate(SLAVES):
            threads.append(GetResults(index))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Resultados
        print('\nResultados:')
        print('    Master: {},     Data: {}\n'.format('localhost', local_date))
        for index, slave in enumerate(SLAVES):
            print('    Salve: {}, Data: {}\n'.format(slave, results[index]))

        print('------------------------------------------------------------')
        time.sleep(10)

if __name__ == '__main__':
    main()
