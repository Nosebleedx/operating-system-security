import socket
import configparser

address = 'localhost'
port = 6060

def add_to_ini(category, entry, filename):
    config = configparser.ConfigParser()
    config.read(filename)

    if not config.has_section(category):
        config.add_section(category)

    config.set(category, entry, entry)

    with open(filename, 'w') as file:
        config.write(file)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((address, port))

config = configparser.ConfigParser()

config.read('entities.ini')
objects = config['for_grand']
vert_values = list(objects.values())


client_login = input('Введите свой логин: ')
client_socket.send(client_login.encode())

aut_answer = client_socket.recv(64).decode()
print(aut_answer)
commands = ['0. Вывести команды',
            '1. Take',
            '2. Grand',
            '3. create',
            '4. remove',
            'stop - to stop']
cmds = ['0', '1', '2', '3', '4', 'stop']
def print_commands():
    print('Список команд:', *commands, sep='\n')

print_commands()

while True:
    if aut_answer == 'Такой сущности не существует.':
        break

    command = input('Введите команду: ')

    while command not in cmds:
        print('Неверная команда')
        command = input('Введите команду: ')

    client_socket.send(command.encode())

    if command == '0':
        print_commands()

    if command == '1':
        u_kogo = input('У кого взять право?: ')
        while u_kogo not in vert_values or u_kogo == client_login:
            print('Некорректный ввод.')
            u_kogo = input('У кого взять право?: ')
        client_socket.send(u_kogo.encode())

        na_chto = input('На что взять право?: ')
        while na_chto not in vert_values or na_chto == client_login:
            print('Некорректный ввод.')
            na_chto = input('На что взять право?: ')
        client_socket.send(na_chto.encode())

        answer = client_socket.recv(64).decode()
        print(answer)

    if command == '2':
        chto_nado = input('Какое право выдать? (t/g/a): ')
        while chto_nado not in ['t', 'g', 'a']:
            print('Некорректный ввод.')
            chto_nado = input('Какое право выдать? (t/g/a): ')
        client_socket.send(chto_nado.encode())

        komu = input('Кому выдать право?: ')
        while komu not in vert_values or komu == client_login:
            print('Некорректный ввод.')
            komu = input('Кому выдать право?: ')
        client_socket.send(komu.encode())

        na_cho = input('На что выдать право?: ')
        while na_cho not in vert_values or na_cho == client_login:
            print('Некорректный ввод.')
            na_cho = input('На что выдать право?: ')
        client_socket.send(na_cho.encode())
        answer = client_socket.recv(64).decode()
        print(answer)
    if command == '3':
        shto = input('Название сущности, которую надо создать?: ')
        while shto in vert_values:
            print(vert_values)
            print('Некорректный ввод.')
            shto = input('Название сущности, которую надо создать?: ')
        client_socket.send(shto.encode())

        add_to_ini('for_grand', shto, 'entities.ini')


        answer = client_socket.recv(128).decode()
        print(answer)
        if answer == (f"Связь от вершины '{client_login}' к вершине '{shto}' успешно создана."):
            vert_values.append(shto)
    if command == '4':
        chto = input('Какую сущность надо удалить?: ')
        while chto not in vert_values:
            print(vert_values)
            print('Некорректный ввод')
            chto = input('Какую сущность надо удалить?: ')
        client_socket.send(chto.encode())
        answer = client_socket.recv(64).decode()
        print(answer)
        if answer == (f"Сущность {chto} удалена."):
            vert_values.remove(chto)
    if command == 'stop':
        client_socket.send('stop'.encode())
        break
client_socket.close()
