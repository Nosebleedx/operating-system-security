import socket
import csv
import configparser

def autentification(login):
    config = configparser.ConfigParser()
    config.read('entities.ini')
    subjects = config['for_take']
    if login in subjects.values():
        return True
    else:
        return False
def read_adjacency_list(csv_file):
    adjacency_dict = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            source, *connections = row
            inner_dict = {}
            for connection in connections:
                target, weight = connection.split(':')
                inner_dict[target] = weight
            adjacency_dict[source] = inner_dict
    return adjacency_dict
def dfs(adjacency_dict, start_vertex, target_vertex, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    visited.add(start_vertex)
    path.append(start_vertex)
    if start_vertex == target_vertex:
        return path
    for neighbor, weight in adjacency_dict.get(start_vertex, {}).items():
        if neighbor not in visited:
            result = dfs(adjacency_dict, neighbor, target_vertex, visited, path)
            if result is not None:
                return result
    path.pop()
    return None
def find_path(adjacency_dict, start_vertex, target_vertex):
    path = dfs(adjacency_dict, start_vertex, target_vertex)
    if path is None:
        return "Пути нет"

    weights = []
    for i in range(len(path) - 1):
        current_vertex = path[i]
        next_vertex = path[i + 1]
        weight = adjacency_dict[current_vertex].get(next_vertex)
        weights.append(weight)

    return weights

def check(rule, paths):
    if rule == 't':
        for i in paths:
            if i not in ['t', 'a']:
                return False
        return True
    if rule == 'g':
        for i in paths:
            if i not in ['g', 'a']:
                return False
        return True
    if rule == 'a':
        for i in paths:
            if i not in ['a']:
                return False
        return True

def grand(rule, chto, komu, na_chto, login, adj_dict):
    frst_condition = check(rule, find_path(adj_dict, login, komu))
    #  Проверка, что от меня есть путь до нужной вершины в виде a or g
    sec_condition = check(chto, find_path(adj_dict, login, na_chto))
    #  Проверка, что от меня есть путь до нужной вершины весом chto или a
    if frst_condition and sec_condition:
        conn.send(f'Ребро весом {chto} можно построить'.encode())
    else:
        conn.send(f'Ребро весом {chto} нельзя построить'.encode())
def take(rule, u_kogo, na_chto, login, adj_dict):
    frst_condition = check(rule, find_path(adj_dict, login, u_kogo))
    #  Проверка, что от меня есть путь до нужной вершины в виде t или a
    sec_condition = check(rule, find_path(adj_dict, u_kogo, na_chto))
    #  Проверка, что у нужной вершины есть путь в вершину у которой надо взять в виде t или a
    if frst_condition and sec_condition:
        conn.send(f'Ребро весом {rule} можно построить'.encode())
    else:
        conn.send(f'Ребро весом {rule} нельзя построить'.encode())

def save_to_csv(adj_dict, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, values in adj_dict.items():
            row = [f"{v}:{w}" for v, w in values.items()]
            writer.writerow([f"{key},{','.join(row)}"])
def create(shto, login, adj_dict):
    #print(adj_dict)
    if shto not in adj_dict:
        adj_dict[shto] = {}
    adj_dict[login][shto] = 'a'
    conn.send(f"Связь от вершины '{login}' к вершине '{shto}' успешно создана.".encode())
    return adj_dict

def remove(chto, rule, login, adj_dict):
    #print(adj_dict)
    if check(rule, find_path(adj_dict, login, chto)):
        for source, connections in adj_dict.items():
            if chto in connections:
                del connections[chto]
            # Удаляем саму вершину chto
        if chto in adj_dict:
            del adj_dict[chto]
        save_to_csv(adj_dict, 'accessGraph.csv')
        conn.send(f'Сущность {chto} удалена.'.encode())
    else:
        conn.send('Не удалось удалить сущность.'.encode())

address = 'localhost'
port = 6060

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((address, port))
server_socket.listen(5)

conn, clientAddr = server_socket.accept()
print(f'{clientAddr} has connected')

login = conn.recv(64).decode()
#print('client Login', login)


adj_dict = read_adjacency_list('accessGraph.csv')
print(adj_dict)


if autentification(login):
    rules = ['t', 'g', 'a']
    print(f'Название сущности: {login}')
    conn.send('Успешный вход в систему.'.encode())
    while True:
        zapros = conn.recv(32).decode()
        if zapros == '1':
            u_kogo = conn.recv(64).decode()
            na_chto = conn.recv(64).decode()
            take(rules[0], u_kogo, na_chto, login, adj_dict)
        if zapros == '2':
            chto = conn.recv(64).decode()
            komu = conn.recv(64).decode()
            na_cho = conn.recv(64).decode()
            grand(rules[1], chto,  komu, na_cho, login, adj_dict)
        if zapros == '3':
            shto = conn.recv(64).decode()
            for_take = 'accessGraph1.csv'
            for_grand = 'accessGraph.csv'
            new_ = create(shto, login, adj_dict)
            print(new_)
            save_to_csv(new_, for_grand)
        if zapros == '4':
            chto = conn.recv(64).decode()
            rule = rules[2]
            remove(chto, rule, login, adj_dict)
            print(adj_dict)
        if zapros == 'stop':
            server_socket.close()
            break
else:
    conn.send('Такой сущности не существует.'.encode())