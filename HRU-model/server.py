import socket
import csv
import configparser



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

def save_dictionary_to_csv(dictionary, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=':', quoting=csv.QUOTE_MINIMAL)
        for key, inner_dict in dictionary.items():
            row = [key]
            for inner_key, value in inner_dict.items():
                row.extend([inner_key, str(value)])
            writer.writerow(row)

def update_ini_file(filename):
    config = configparser.ConfigParser()
    config.read('entities.ini')
    objects = config['objects']
    if filename in objects:
        del objects[filename]

    with open('entities.ini', 'w') as configfile:
        config.write(configfile)

def autentification(login):
    config = configparser.ConfigParser()
    config.read('entities.ini')
    subjects = config['subjects']
    if login in subjects.values():
        return True
    else:
        return False

def read(filename, matrix_cons):
    #print(filename, matrix_cons)
    if int(matrix_cons[filename]) >= 1:
        conn.send('Success reading.'.encode())
    else:
        conn.send("You can't do it.".encode())
    pass

def write(filename, matrix_cons, message):
    #print(filename, matrix_cons, message)
    if int(matrix_cons[filename]) >= 2:
        print(f'Запись сообщения "{message}"')
        conn.send('Success writing.'.encode())
    else:
        conn.send("You can't do it.".encode())

def delete(filename, matrix_cons, subjects_list, matrix_dict):
    #print(filename, matrix_cons, subjects_list, sep='  |||  ')
    if int(matrix_cons[filename]) == 3:
        for i in range(len(subjects_list)):
            matrix_dict[subjects_list[i]].pop(filename)
            save_dictionary_to_csv(matrix_dict, 'matrix.csv')
            update_ini_file(filename)
        conn.send('Success delete.'.encode())
        #print(filename, matrix_cons, subjects_list, sep='  |||  ')
    else:
        conn.send("You can't do it.".encode())

def give_rule(subj_name, id_rule, filename, login, matrix_dict):
    #print(matrix_dict[subj_name][filename], matrix_dict[login][filename], sep='  ||  ')
    if matrix_dict[login][filename] == 4:
        if id_rule == 4:
            conn.send("You can't make second owner")
        else:
            conn.send('Success give rule'.encode())
            matrix_dict[subj_name][filename] = id_rule
            save_dictionary_to_csv(matrix_dict, 'matrix.csv')
    else:
        conn.send("You can't do it".encode())

'''
admin:file1:3:file2:3:file3:3
user:file1:0:file2:0:file3:0
'''

address = 'localhost'
port = 6868

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((address, port))
server_socket.listen(5)

conn, clientAddr = server_socket.accept()
print(f'{clientAddr} has connected')



matrix_dict = read_matrix('matrix.csv')
login = conn.recv(32).decode()
print(matrix_dict)
config = configparser.ConfigParser()
config.read('entities.ini')
subjects = config['subjects']
subject_values = list(subjects.values())
print('subjects:', subject_values)

if autentification(login):
    rules = [0, 1, 2, 3, 4]  # when 0 - null, 1 - read, 2 - write, 3 - delete, 4 - owner
    print(f'Логин субъекта: {login}')
    print(f'Связь субьекта "{login}" с объектами: \n {matrix_dict[login]}')
    print(rules, '- правила, где 0 - null, 1 - read, 2 - write, 3 - delete, 4 - owner')
    conn.send('Успешный вход в систему.'.encode())
    while 1:
        zapros = conn.recv(32).decode()
        if zapros == '1':
            filename = conn.recv(32).decode()
            read(filename, matrix_dict[login])
        if zapros == '2':
            filename = conn.recv(32).decode()
            message = conn.recv(64).decode()
            write(filename, matrix_dict[login], message)
        if zapros == '3':
            filename = conn.recv(32).decode()
            delete(filename, matrix_dict[login], subject_values, matrix_dict)
            # filename, Связь субьекта "admin" с объектами, все субъекты
        if zapros == '4':
            subj_name = conn.recv(32).decode()
            filename = conn.recv(32).decode()
            id_rule = conn.recv(32).decode()
            #print(subj_name, id_rule, matrix_dict[subj_name], filename, login, matrix_dict, sep='\n')
            give_rule(subj_name,
                      id_rule,
                      filename,
                      login,
                      matrix_dict)
            #  Имя субъекта кому надо дать право, номер права, словарь которым владеет тот кому надо дать право, имя объекта на которое надо дать право, связь
        if zapros == 'stop':
            server_socket.close()
            break
else:
    conn.send('Такого пользователя не существует.'.encode())
    server_socket.close()