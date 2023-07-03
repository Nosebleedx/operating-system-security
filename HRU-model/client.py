import socket
import configparser

address = 'localhost'
port = 6868

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((address, port))

config = configparser.ConfigParser()

config.read('entities.ini')
objects = config['objects']
object_values = list(objects.values())
subjects = config['subjects']
subjects_values = list(subjects.values())

client_login = input('Введите свой логин: ')
client_socket.send(client_login.encode())

aut_answer = client_socket.recv(64).decode()
print(aut_answer)
commands = ['0. Вывести команды',
            '1. Чтение файла',
            '2. Запись в файл',
            '3. Удаление файла',
            '4. Дать право',
            'stop - to stop']
cmds = ['0', '1', '2', '3','4', 'stop']
def print_commands():
    print('Список команд:', *commands, sep='\n')

print_commands()

while True:
    if aut_answer == 'Такого пользователя не существует.':
        break

    command = input('Введите команду: ')
    while command not in cmds:
        print('Неверная команда')
        command = input('Введите команду: ')
        if command in cmds:
            continue
    client_socket.send(command.encode())


    if command in ['0']:
        print_commands()

    if command in ['1', '3']:
        print(object_values)
        file_name = input('Введите название объекта: ')
        if file_name not in object_values:
            while file_name not in object_values:
                print('Такого объекта не существует')
                file_name = input('Введите название объекта: ')
        client_socket.send(file_name.encode())
        if command == '3':
            object_values.remove(file_name)

        answer = client_socket.recv(16).decode()
        print(answer)
    if command in ['2']:
        print(object_values)
        file_name = input('Введите название объекта: ')
        if file_name not in object_values:
            while file_name not in object_values:
                print('Такого объекта не существует')
                file_name = input('Введите название объекта: ')
        message = input('Введите запись: ')
        client_socket.send(file_name.encode())
        client_socket.send(message.encode())

        answer = client_socket.recv(64).decode()
        print(answer)

    if command in ['4']:

        print(subjects_values)
        subj_name = input('Имя субъекта, кому выдаётся право: ')
        while subj_name not in subjects_values or subj_name == client_login:
            print('Ошибка.')
            subj_name = input('Имя субъекта, кому выдаётся право: ')
        client_socket.send(subj_name.encode())

        print(object_values)
        filename = input('Введите имя объекта, на которое выдаётся право: ')
        if filename not in object_values:
            while filename not in object_values:
                print('Такого объекта не существует')
                filename = input('Введите имя объекта, на которое выдаётся право: ')
                if filename in object_values:
                    continue
        client_socket.send(filename.encode())

        print(['0', '1', '2', '3', '4'])
        id_rule = input('Номер права, которое выдаётся субъекту: ')
        if id_rule not in ['0', '1', '2', '3','4']:
            while id_rule not in ['0', '1', '2', '3','4']:
                print('Некорректный номер права')
                id_rule = input('Номер права, которое выдаётся субъекту: ')
        client_socket.send(id_rule.encode())

        answer = client_socket.recv(32).decode()
        print(answer)

    if command == 'stop':
        client_socket.send('stop'.encode())
        break

client_socket.close()
