import sympy
import socket
import random


ROUNDS = 21
def prime_number(n):
    prime_number = sympy.randprime(1, n - 1)
    return prime_number * 4 + 3

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

N = int(client_socket.recv(4096).decode())
secret = prime_number(N)
V = secret**2 % N
client_socket.send(str(V).encode())

#secret = 124562145141312434123



cnt = 0
while cnt != ROUNDS:

    rand_r = random.randint(1, N - 1)
    x = rand_r ** 2 % N
    client_socket.send(str(x).encode())
    bit_e = int(client_socket.recv(2).decode())
    print(f"rand_r = {rand_r}, x_number = {x}, bit_e = {bit_e}")
    if bit_e == 0:
        Y = rand_r
        client_socket.send(str(Y).encode())
    else:
        Y = rand_r * secret ** bit_e % N
        client_socket.send(str(Y).encode())
    answer = client_socket.recv(32).decode()
    cnt += 1
    print(f'ROUND {cnt}: Answer - {answer}')

