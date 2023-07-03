import hashlib
import socket
import configparser

config = configparser.ConfigParser()
config.read("EnterPass.ini")

# Connection functions
def open_server(ip_addres, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_addres, port))
    server_socket.listen(1)
    client_socket, client_addres = server_socket.accept()
    print(f"Подключился чудик: {client_addres}")
    return client_socket

def connect(ip_addres, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_addres, port))
    return client_socket

def send(client_socket, msg):
    client_socket.send(str(msg).encode())

def take(client_socket):
    message = int(client_socket.recv(1024).decode())
    return message

# Verification functions
def hash_n_times(p, n, A):
    p_bytes = p.to_bytes((p.bit_length() + 7) // 8, byteorder='big')
    for i in range(n - A + 1):
        hash_obj = hashlib.sha256(p_bytes)
        p_bytes = hash_obj.digest()
    return int.from_bytes(p_bytes, byteorder='big')

def set_value_in_property_file(file_path, section, key, value):
    config = configparser.RawConfigParser()
    config.read(file_path)
    config.set(section,key,value)
    cfgfile = open(file_path,'w')
    config.write(cfgfile, space_around_delimiters=False)
    cfgfile.close()

client_socket = open_server("localhost", 9999)

# Verification settings
hashreg = take(client_socket)
login = str(config['database']['login'])
A_number = int(config['database']['A_number'])
dict = {login: A_number}
#reg_acc = hash_n_times()
N_times = 100000
A = A_number
old_A = None
hashed = None

secret = hash_n_times(hashreg, N_times, A)

while True:
    if old_A != A:
        old_A = A
        send(client_socket, A)
        hashed = take(client_socket)
        hashed = hash_n_times(hashed, 0, 0)
        if hashed == secret:
            print(hashed, secret, A)
            msg = 'Успех'
            send(client_socket, msg)
            print(dict)
            A += 1
            set_value_in_property_file('EnterPass.ini', 'database', 'A_number', str(A))
            secret = hash_n_times(hashreg, N_times, A)
        else:
            msg = 'Провал'
            print(msg)
            send(client_socket, msg)
