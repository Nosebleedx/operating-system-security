import socket
import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, name_db):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=name_db
        )
        print('Succesfull Connected to db')
    except Error as e:
        print(f'Error!!!!!!!!! ->>> {e}')
    return connection

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 10000))
sock.listen(10)

connect = create_connection("localhost", "root", "", "bos")
choice = '1'

while True:
    connection, addr = sock.accept()
    connection.send('Вход'.encode())
    print('Подключился чудик:', addr)
    choice = connection.recv(4)
    if choice.decode() == '1':
        print('Вошёл чудик!')
        login = connection.recv(32).decode()
        cur = connect.cursor()
        cur.execute(f"SELECT * FROM `account` WHERE `UserName` LIKE '{login}'")
        result = cur.fetchall()
        if result == []:
            connection.send('Неверный логин или пароль!'.encode())
        else:
            login_bd = result[0][1]
            hash_bd = result[0][2]
            salt_bd = result[0][3]
            connection.sendall(salt_bd.encode())
            hash_key = connection.recv(256).decode()

            print('Его логин:', login)
            print('Hash:', hash_key)

            if login_bd == login and hash_key == hash_bd:
                print('Аутентификация пройдена')
                connection.send('Аутентификация пройдена'.encode())
            else:
                print("Что-то пошло не так")
                print('Аутентификация не пройдена. \nНеверный логин или пароль.')
                connection.send('Аутентификация не пройдена. \nНеверный логин или пароль.'.encode())