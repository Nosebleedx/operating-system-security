import hashlib
import configparser
import socket

config = configparser.ConfigParser()
config.read("EnterPass.ini")

def hash_password(login, password):
    password_bytes = password.encode('utf-8')
    servername_bytes = login.encode('utf-8')
    hash_obj = hashlib.sha256(password_bytes + servername_bytes)
    p_hex = hash_obj.hexdigest()
    p = int(p_hex, 16)

    return p

def hash_n_times(p, n):
    p_bytes = p.to_bytes((p.bit_length() + 7) // 8, byteorder='big')
    for i in range(n):
        hash_obj = hashlib.sha256(p_bytes)
        p_bytes = hash_obj.digest()
        p_n = int.from_bytes(p_bytes, byteorder='big')
    return p_n

def conn_server(ip_address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ((ip_address, port))
    client_socket.connect(server_address)
    return client_socket

def send(client_socket, msg):
    client_socket.send(str(msg).encode())

def take(client_socket):
    message = int(client_socket.recv(1024).decode())
    return message

def take_str(client_socket):
    message = client_socket.recv(64).decode()
    return message

def main():
    N_times = 100000
    counter_ident = 5
    login = str(config['database']['login'])
    password = str(config['database']['pass'])
    N = 100000
    cnt = 1
    A = None
    old_A = 0
    hashed = None
    na_times = None

    p = hash_password(login, password)

    client_socket = conn_server("localhost", 9999)
    send(client_socket, p)

    while True:
        if cnt <= counter_ident:
            old_A = A
            A = take(client_socket)
            login = input('Введите логин ')
            password = input('Введите пароль ')
            hashed = hash_password(login, password)
            if old_A != A:
                na_times = N_times - A
                hashed = hash_n_times(hashed, na_times)
                send(client_socket, hashed)
                answer = take_str(client_socket)
                print(f"Попытка номер {cnt} - " + answer)
                cnt +=1
                print(f'Попыток осталось: {counter_ident - cnt}')
        else:
            print('Количество попыток закончилось')
            break

if __name__ == '__main__':
    main()