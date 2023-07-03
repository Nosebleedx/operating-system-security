import json

def read_json(filename):
    with open(filename, 'r') as file:
        main_dict = json.load(file)
        return main_dict
def display_role_matrix(data):
    subjects = data["subjects"]
    objects = list(data["objects"].keys())

    role_matrix = []
    for subject in subjects:
        row = []
        for obj in objects:
            available_roles = []
            for role, role_data in data["roles"].items():
                if subject in role_data["subjects"] and obj in role_data["objects"]:
                    available_roles.append(role)
            row.append(available_roles)
        role_matrix.append(row)

    print("Матрица ролей:")
    print("Subjects/Objects", end="\t\t")
    for obj in objects:
        print(obj, end="\t\t")
    print()

    for i, subject in enumerate(subjects):
        print(subject, end="\t\t\t")
        for j, obj in enumerate(objects):
            roles = role_matrix[i][j]
            print(roles, end="\t\t")
        print()
def print_commands():
    print('Список команд:', *commands, sep='\n')

def check_adj_subj(parents, main_dict):
    result = []
    for i in range(len(parents)):
        result.append(main_dict['roles'][parents[i]]['subjects'])
    ne_set = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            ne_set.append(result[i][j])
    result = list(set(ne_set))
    if result == []:
        return 'Смежных субъектов нет'
    return result


def check_psbl_rghts(main_dict, parents, obj):
    result = []

    for i in range(len(parents)):
        if obj in main_dict['roles'][parents[i]]['objects']:
            result.append(main_dict['roles'][parents[i]]['objects'][obj])

    ne_set = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            ne_set.append(result[i][j])

    result = list(set(ne_set))
    return result
def create_role(role_name, avlbl_sbj, psbl_rght, obj, rght_plus, main_dict):
    res_rghts = psbl_rght + rght_plus
    if 'roles' not in main_dict:
        main_dict['roles'] = {}
    if role_name not in main_dict['roles']:
        main_dict['roles'][role_name] = {'subjects': [], 'objects': {}}
    main_dict['roles'][role_name]['subjects'] = [i for i in avlbl_sbj]
    main_dict['roles'][role_name]['objects'][obj] = res_rghts



main_dict = read_json('roles.json')
roles = list(main_dict['roles'].keys())
rules = ['read', 'write', 'delete', 'execute']
print(main_dict)

commands = ['0. Показать команды',
            '1. Создать роль',
            '2. Показать матрицу ролей',
            'stop - to stop']
cmds = ['0', '1', '2', '3', 'stop']
print_commands()
while True:
    command = input('Введите команду: ')
    while command not in cmds:
        print('Некорректный ввод.')
        command = input('Введите команду: ')

    if command in ['0']:
        print_commands()

    if command in ['1']:
        print(roles)
        role_name = input('Введите название роли: ')
        if role_name in roles:
            print('Роль с таким названием уже существует.')
            role_name = input('Введите название роли: ')
        print(roles)
        parents = []
        for i in range(1, len(roles) + 1):
            parent = input(f'Введите название {i} родителя: ')
            if parent == '':
                break
            while parent not in roles:
                print('Такого родителя не существует')
                parent = input(f'Введите название {i} родителя: ')
            parents.append(parent)

        avlbl_sbj = check_adj_subj(parents, main_dict)
        print(f'Доступные субъекты: {", ".join(avlbl_sbj)}')
        if avlbl_sbj == ['Смежных субъектов нет']:
            print('Это будет пустая роль.')
            break

        sbj_input = input('Введите название субъекта (можно ввести несколько через запятую): ')
        sbj_list = [subj.strip() for subj in sbj_input.split(",")]

        while not all(subj in avlbl_sbj for subj in sbj_list):
            print('Некорректный ввод')
            sbj_input = input('Введите название субъекта (можно ввести несколько через запятую): ')
            sbj_list = [subj.strip() for subj in sbj_input.split(",")]

        subjects_list = [subj.strip() for subj in sbj_input.split(",")]

        print(list(main_dict['objects'].keys()))
        obj = input('Введите название объекта: ')
        while obj not in list(main_dict['objects'].keys()):
            print('Такого объекта не существует')
            obj = input('Введите название объекта')


        psbl_rght = check_psbl_rghts(main_dict, parents, obj)
        print(f'Уже доступные права: {psbl_rght}')
        rght_plus = []
        for i in range(len(rules)):
            if rules[i] not in psbl_rght:
                rght_plus.append(rules[i])
        print('Возможно добавление прав: ', rght_plus)
        for i in range(len(rght_plus)):
            print('Да || Нет')
            client_ans = input(f'Добавить право: |{rght_plus[i]}|?: ')
            while client_ans not in ['Да', 'Нет']:
                print('Да || Нет')
                client_ans = input(f'Добавить право: |{rght_plus[i]}|?: ')
            if client_ans == 'Да':
                pass
            else:
                rght_plus.remove(rght_plus[i])

        create_role(role_name, subjects_list, psbl_rght, obj, rght_plus, main_dict)
        print('Роль успешно создана')
        print(role_name,':', main_dict['roles'][role_name])
        print(main_dict)
        with open('roles.json', 'w') as wr_file:
            json.dump(main_dict, wr_file)

    if command in ['2']:
        display_role_matrix(main_dict)

    if command == 'stop':
        break

