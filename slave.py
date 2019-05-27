import socket
import time
from Clock import Clock
import math


r = Clock()
udp_ip = ""
udp_port = 7101
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((udp_ip, udp_port))

while True:
    # Recebe a porta que o slave enviará seu clock
    mensage, addr = sock.recvfrom(1024)
    print("Mensagem recebida:", mensage.decode())
    port = int(mensage.decode())
    # Envia o clock para o master
    sock.sendto((str(r.getClock())).encode(), (addr[0], port))
    # Recebe a quantidade que deve ser ajustada
    mensage, addr = sock.recvfrom(1024)
    # Imprime os valores antes do ajuste
    print(r.getClock())
    print(r.getDate())
    # Ajusta o clock de acordo com o valor passado
    print("Ajustar em: ", mensage)
    r.adjustClock(int(mensage.decode()))
    # Imprime os valores após os ajustes
    print(r.getClock())
    print(r.getDate())
    # Envia sua "Data" para o master printar e comparar os resultados
    sock.sendto(r.getDate().encode(), (addr[0], port))
