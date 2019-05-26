import socket
import time
from Clock import Clock
import math


r = Clock()

udp_ip = "127.0.0.1"
udp_port = 7101
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((udp_ip, udp_port))
mensage, addr = sock.recvfrom(1024) # Tamanho do buffer eh 1024 bytes
print ("Mensagem recebida:", mensage)
sock.sendto((str(r.getClock())).encode() , addr)
mensage, addr = sock.recvfrom(1024)
print("Ajustar em: ", mensage)
print("Erro é : ", r.getError())
print(r.getClock())
print(r.getDate())

r.adjustClock(int(math.trunc(float(mensage.decode()))))
print(r.getClock())
print(r.getDate())


