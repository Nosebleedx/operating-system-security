import socket
import configparser




client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 6868))

client_login = input('Введите название субъекта: ')
client_socket.send(client_login.encode())

aut_answer = client_socket.recv(64).decode()

config = configparser.ConfigParser()
config.read('entities.ini')
objects = config['object_values']
object_values = list(objects.values())
subjects = config['subjects_values']
subject_values = list(subjects.values())

commands = ['0. Вывести команды',
            '1. Создание объекта',
            '2. Чтение объекта',
            '3. Запись в объект',
            '4. Удаление объекта',
            '5. Установить мандат объекту',
            'stop - to stop']
cmds = ['0', '1', '2', '3', '4', '5', 'stop']
def print_commands():
    print('Список команд:', *commands, sep='\n')

print_commands()

sec_levels = [0, 1, 2, 3]
#  0 - null, 1 - secret, 2 - SuperSecret, 3 - SpecialImportance <---

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

    if command in ['1']:

        filename = input("Введите название объекта: ")
        while filename in object_values:
            print('Объект с таким именем уже существует.')
            filename = input("Введите название объекта")
        object_values.append(filename)
        client_socket.send(filename.encode())

        print('Метки безопасности: ', sec_levels)
        my_sec_lev = int(client_socket.recv(4).decode())
        print(my_sec_lev)
        seclev = int(input('Введите мандат, выдаваемый созданному объекту: '))
        while seclev > my_sec_lev or seclev not in sec_levels:
            print('Некорректный ввод')
            seclev = int(input("Введите мандат: "))
        client_socket.send(str(seclev).encode())

        material = input("Начальная запись в объекте: ")
        client_socket.send(material.encode())

        answer = client_socket.recv(64).decode()
        print(answer)

    if command in ['2']:
        print(object_values)
        chto = input('Что прочитать?: ')
        while chto not in object_values:
            print('Такого объекта не существует')
            chto = input('Что прочитать?: ')
        client_socket.send(chto.encode())

        answer = client_socket.recv(64).decode()
        print(answer)

        material = client_socket.recv(256).decode()
        print(f'Содержимое объекта - {material}')

    if command in ['3']:
        print(object_values)
        kuda = input('Куда записать?: ')
        while kuda not in object_values:
            print('Такого объекта не существует')
            shto = input('Куда записать?: ')
        client_socket.send(kuda.encode())
        material = input('Что записвть?')
        client_socket.send(material.encode())

        answer = client_socket.recv(64).decode()
        print(answer)

    if command in ['4']:
        print(object_values)
        che = input('Что удалить?: ')
        while che not in object_values:
            print('Такого объекта не существует')
            che = input('Что удалить?: ')
        client_socket.send(che.encode())

        answer = client_socket.recv(64).decode()
        print(answer)
        if answer == 'Successfull delete object':
            object_values.remove(che)

    if command in ['5']:
        print(object_values, subject_values)
        komy = input('Кому|Чему установить мандат?: ')
        while komy not in object_values and komy not in subject_values:
            print('Такой сущности не существует')
            komy = input('Кому|Чему установить мандат?: ')
        client_socket.send(komy.encode())

        print(sec_levels)
        sc = input('Какой мандат установить сущности?: ')
        while sc not in ['0', '1', '2', '3']:
            print('Некорректный ввод.')
            sc = input('Какой мандат установить сущности?: ')
        client_socket.send(str(sc).encode())

        answer = client_socket.recv(64).decode()
        print(answer)


    if command == 'stop':
        client_socket.send('stop'.encode())
        break


client_socket.close()