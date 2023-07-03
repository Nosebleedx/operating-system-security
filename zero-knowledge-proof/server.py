import socket
import sympy
from bbs import generate_e


def prime_number():
    prime_number = sympy.randprime(2**1023, 2**1024 - 1)
    return prime_number * 4 + 3



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 9999))
server_socket.listen(5)
client_socket, client_address = server_socket.accept()
print(f'Подключился чудик {client_address}')

p = prime_number()
q = prime_number()
N = p * q

client_socket.send(str(N).encode())
V = int(client_socket.recv(4096).decode())

while True:
    X = int(client_socket.recv(2048).decode())
    bit_e = int(generate_e())
    client_socket.send(str(bit_e).encode())
    Y = int(client_socket.recv(2048).decode())
    verif = X * V ** bit_e % N
    print(f'Y = {Y}, Y**2%N = {Y**2%N}, XV**bit_e%N = {verif}')
    if Y**2 % N ==  verif:
        msg = 'Accept'
        client_socket.send(msg.encode())
    else:
        msg = 'FAIL'
        client_socket.send(msg.encode())
        break
