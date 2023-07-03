import socket
import csv
from configparser import ConfigParser

def autentification(login):
    config = ConfigParser()
    config.read('entities.ini')
    subjects = config['subjects_values']
    if login in subjects.values():
        return True
    else:
        return False
def read_matrix(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=':')
        matrix_dict = {}
        for row in reader:
            login = row[0]
            pairs = row[1:]
            matrix_dict[login] = {}
            for i in range(0, len(pairs), 2):
                file_name = pairs[i]
                weight = int(pairs[i + 1])
                matrix_dict[login][file_name] = weight
    #print("Словарь матрицы доступа:", matrix_dict)
    return matrix_dict
def create_subject_dict(file_name):
    parser = ConfigParser()
    parser.read(file_name)

    subject_dict = {}
    if 'subjects' in parser:
        subjects_section = parser['subjects']
        keys = [key for key in subjects_section if key.startswith('login')]
        for key in keys:
            value_login = subjects_section[key]
            value_sc = subjects_section.get(f"sc{key.split('login')[1]}")
            if value_sc:
                value_sc = value_sc.strip()
            subject_dict[value_login] = [value_sc, value_sc]

    return subject_dict
def create_object_dict(file_name, category):
    parser = ConfigParser()
    parser.read(file_name)

    object_dict = {}
    if category in parser:
        objects_section = parser[category]
        keys = [key for key in objects_section if key.startswith('file')]
        for key in keys:
            value_key = objects_section[key]
            value_sc = objects_section.get(f"sc{key.split('file')[1]}")
            if value_sc:
                value_sc = value_sc.strip()
            object_dict[value_key] = [value_sc, 'smth']

    return object_dict

def backup_matrix(filename, matrix):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=':')
        for key, value in matrix.items():
            row = [key]
            for obj, access in value.items():
                row.append(obj)
                row.append(str(access))
            writer.writerow(row)

def create(filename, seclev, material, matrix_dict, objects):
    for key in matrix_dict:
        matrix_dict[key][filename] = 0
    objects[filename] = [str(seclev), material]
    backup_matrix('matrix.csv', matrix_dict)
    parser = ConfigParser()
    parser.read('entities.ini')

    if 'object_values' not in parser:
        parser['object_values'] = {}

    parser['object_values'][filename] = filename
    if 'objects' not in parser:
        parser['objects'] = {}

    parser['objects'][f'file{len(objects)}'] = filename
    parser['objects'][f'sc{len(objects)}'] = str(seclev)

    with open('entities.ini', 'w') as config_file:
        parser.write(config_file)

    return matrix_dict, objects

def read(filename, my_seclev, temp_sc,  his_seclev, matrix_dict, login, subjects, objects_dict):
    if his_seclev > temp_sc:
        if his_seclev > my_seclev:
            conn.send('No read up.'.encode())
    elif his_seclev <= temp_sc:
        conn.send("Successfull reading.".encode())
        conn.send(objects_dict[filename][1].encode())
    elif his_seclev <= my_seclev:
        conn.send("Successfull reading.".encode())
        conn.send(objects_dict[filename][1].encode())
        matrix_dict[login][filename] = int(objects_dict[filename][0])  # заполнение слота в matrix
        backup_matrix('matrix.csv', matrix_dict)
        subjects[login][1] = str(objects_dict[filename][0])  # замена seclev у subj
        # проверка на остальные мандаты этого subject
        key_list = list(matrix_dict[login].keys())
        for i in key_list:
            if matrix_dict[login][i] > int(subjects[login][1]):
                matrix_dict[login][i] = 0

def write(kuda, material, my_sc, temp_sc, his_sc, matrix_dict, login, subjects, objects_dict):
    if his_sc < temp_sc:
        temp_scc = his_sc
        if his_sc == temp_scc:
            conn.send(f"Successfull writing material - {material}".encode())
            matrix_dict[login][kuda] = int(objects_dict[kuda][0])  # заполнение слота в matrix
            backup_matrix('matrix.csv', matrix_dict)
            subjects[login][1] = str(objects_dict[kuda][0])  # замена seclev у subj
            objects_dict[kuda][1] = material  # Заменяет запись

            # проверка на остальные мандаты этого subject
            key_list = list(matrix_dict[login].keys())
            for i in key_list:
                if matrix_dict[login][i] > int(subjects[login][1]):
                    matrix_dict[login][i] = 0

    elif his_sc > temp_sc:
        if my_sc == his_sc:
            conn.send(f"Successfull writing material - {material}".encode())
            matrix_dict[login][kuda] = int(objects_dict[kuda][0])  # заполнение слота в matrix
            backup_matrix('matrix.csv', matrix_dict)
            subjects[login][1] = str(objects_dict[kuda][0])  # замена seclev у subj
            objects_dict[kuda][1] = material  # Заменяет запись

            # проверка на остальные мандаты этого subject
            key_list = list(matrix_dict[login].keys())
            for i in key_list:
                if matrix_dict[login][i] > int(subjects[login][1]):
                    matrix_dict[login][i] = 0
        elif my_sc < his_sc:
            conn.send(f"Successfull writing material - {material}".encode())
            matrix_dict[login][kuda] = int(objects_dict[kuda][0])  # заполнение слота в matrix
            backup_matrix('matrix.csv', matrix_dict)
            subjects[login][1] = str(objects_dict[kuda][0])  # замена seclev у subj
            objects_dict[kuda][1] += material  # Запись в выше не заменяет запись

            # проверка на остальные мандаты этого subject
            key_list = list(matrix_dict[login].keys())
            for i in key_list:
                if matrix_dict[login][i] > int(subjects[login][1]):
                    matrix_dict[login][i] = 0

def delete(chto, my_sc, temp_sc, his_sc, matrix_dict, objects_dict):
    if his_sc > temp_sc and his_sc > my_sc:
        conn.send("You can't delete this object.".encode())
    elif his_sc <= temp_sc:
        conn.send("Successfull delete object".encode())
        mat_keys = list(matrix_dict.keys())  # Del from matrix
        for i in mat_keys:
            del matrix_dict[i][chto]
            backup_matrix('matrix.csv', matrix_dict)
        del objects_dict[chto]  # Del from dict
        # Del from ini file
        config = ConfigParser()
        config.read('entities.ini')
        config.remove_option('objects', chto)
        config.remove_option('objects', f'sc{len(objects_dict) + 1}')
        with open('entities.ini', 'w') as configfile:
            config.write(configfile)
        config.read('entities.ini')
        config.remove_option('object_values', chto)
        with open('entities.ini', 'w') as configfile:
            config.write(configfile)
    elif his_sc <= my_sc:
        conn.send("Successfull delete object".encode())
        mat_keys = list(matrix_dict.keys())  # Del from matrix
        for i in mat_keys:
            del matrix_dict[i][chto]
            backup_matrix('matrix.csv', matrix_dict)
        del objects_dict[chto]  # Del from dict
        # Del from ini file
        config = ConfigParser()
        config.read('entities.ini')
        config.remove_option('objects', chto)
        config.remove_option('objects', f'sc{len(objects_dict) + 1}')
        with open('entities.ini', 'w') as configfile:
            config.write(configfile)
        config.read('entities.ini')
        config.remove_option('object_values', chto)
        with open('entities.ini', 'w') as configfile:
            config.write(configfile)

def set_sc(komy, chto, my_sc, temp_sc, his_sc, matrix_dict, login,  objects_dict, subjects):
    if his_sc > temp_sc:
        if his_sc > my_sc:
            conn.send("You can't change his secr. lvl.".encode())
    elif his_sc <= temp_sc:
        conn.send('Successfull set secr.lvl.'.encode())
        objects_dict[komy][0] = str(chto)
    elif his_sc <= my_sc:
        conn.send('Successfull set secr.lvl.'.encode())
        objects_dict[komy][0] = str(chto)
        subjects[login][1] = str(objects_dict[komy][0])
        key_list = list(matrix_dict[login].keys())
        for i in key_list:
            if matrix_dict[login][i] > int(subjects[login][1]):
                matrix_dict[login][i] = 0


'''
client1:file1:0:file2:0:file3:0:file4:0
client2:file1:0:file2:0:file3:0:file4:0
client3:file1:0:file2:0:file3:0:file4:0
'''

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 6868))
server_socket.listen(5)

conn, clientAddr = server_socket.accept()
print(f'{clientAddr} has connected.')

print('---------------------------------------------------------------------')
matrix_dict = read_matrix('matrix.csv')
print(f'MATRIX: {matrix_dict}')
print('---------------------------------------------------------------------')
objects_dict = create_object_dict('entities.ini', 'objects')
print(f'OBJECTS: {objects_dict}')
print('---------------------------------------------------------------------')
subjects_dict = create_subject_dict('entities.ini')
print(f'SUBJECTS: {subjects_dict}')
print('---------------------------------------------------------------------')

login = conn.recv(64).decode()

if autentification(login):
    sec_levels = [0, 1, 2, 3]
    #  0 - null, 1 - secret, 2 - SuperSecret, 3 - SpecialImportance <---
    print(f'Логин субъекта: {login}')
    print(f'Матрица доступа "{login}" с объектами: \n {matrix_dict[login]}')
    print(sec_levels, '- мандаты, где  0 - null, 1 - secret, 2 - SuperSecret, 3 - SpecialImportance')
    print("----------------------------------------------------------------------------------------")
    conn.send('Успешный вход в систему.'.encode())
    while True:
        zapros = conn.recv(32).decode()
        if zapros == '1':
            filename = conn.recv(64).decode()
            my_sec_lev = int(subjects_dict[login][0])
            conn.send(str(my_sec_lev).encode())
            seclev = int(conn.recv(64).decode())
            material = conn.recv(256).decode()
            matrix_dict, objects_dict = create(filename, seclev, material,
                                               matrix_dict, objects_dict)
            conn.send('Объект успешно создан.'.encode())

            print(f'MATRIX: {matrix_dict}')
            print('---------------------------------------------------------------------')
            print(f'OBJECTS: {objects_dict}')

        if zapros == '2':
            chto = conn.recv(64).decode()
            print(chto)
            my_sec_lev = int(subjects_dict[login][0])
            temp_sec_lev = int(subjects_dict[login][1])
            obj_sec_lev = int(objects_dict[chto][0])
            print(my_sec_lev, obj_sec_lev, sep='   ||  ')
            read(chto, my_sec_lev, temp_sec_lev, obj_sec_lev,
                 matrix_dict, login, subjects_dict, objects_dict)

            print(f'MATRIX: {matrix_dict}')
            print('---------------------------------------------------------------------')
            print(f'OBJECTS: {objects_dict}')
            print('---------------------------------------------------------------------')
            print(f'SUBJECTS: {subjects_dict}')

        if zapros == '3':
            kuda = conn.recv(64).decode()
            material = conn.recv(256).decode()
            my_sec_lev = int(subjects_dict[login][0])
            temp_sec_lev = int(subjects_dict[login][1])
            obj_sec_lev = int(objects_dict[kuda][0])
            write(kuda, material, my_sec_lev, temp_sec_lev, obj_sec_lev,
                  matrix_dict, login, subjects_dict, objects_dict)
            print(f'MATRIX: {matrix_dict}')
            print('---------------------------------------------------------------------')
            print(f'OBJECTS: {objects_dict}')
            print('---------------------------------------------------------------------')
            print(f'SUBJECTS: {subjects_dict}')

        if zapros == '4':
            che = conn.recv(64).decode()
            my_sec_lev = int(subjects_dict[login][0])
            temp_sec_lev = int(subjects_dict[login][1])
            obj_sec_lev = int(objects_dict[che][0])
            delete(che, my_sec_lev, temp_sec_lev,
                   obj_sec_lev, matrix_dict, objects_dict)
            print(f'MATRIX: {matrix_dict}')
            print('---------------------------------------------------------------------')
            print(f'OBJECTS: {objects_dict}')
            print('---------------------------------------------------------------------')
            print(f'SUBJECTS: {subjects_dict}')

        if zapros == '5':
            komy = conn.recv(32).decode()
            chto = conn.recv(32).decode()
            my_sec_lev = int(subjects_dict[login][0])
            temp_sec_lev = int(subjects_dict[login][1])
            obj_sec_lev = int(objects_dict[komy][0])
            set_sc(komy, chto, my_sec_lev, temp_sec_lev,
                       obj_sec_lev, matrix_dict, login, objects_dict, subjects_dict)

            print(f'MATRIX: {matrix_dict}')
            print('---------------------------------------------------------------------')
            print(f'OBJECTS: {objects_dict}')
            print('---------------------------------------------------------------------')
            print(f'SUBJECTS: {subjects_dict}')

        if zapros == 'stop':
            server_socket.close()
            break
else:
    conn.send('Такого пользователя не существует.'.encode())