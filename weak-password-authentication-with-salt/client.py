import socket
import hashlib
import configparser


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 10000))

config = configparser.ConfigParser()
config.read('config.ini')


choice = config['valid_user']['choice']
password = config['valid_user']['password']
login = config['valid_user']['login']

run = True

while run:
    data = sock.recv(512).decode()
    sock.send(choice.encode())
    print(data)
    if choice == '1':

        sock.send(login.encode())
        sal = sock.recv(256)
        sal = bytearray(sal)
        hash_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), sal, 100000).hex()
        sock.send(hash_key.encode())
        print(choice)
        print(f'Login: {login} \nPassword: {password} \nHash: {hash_key}')

