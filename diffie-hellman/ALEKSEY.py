import socket
import sympy
import gmpy2

def create_private_key():
    pri_key = sympy.randprime(2 ** 255, 2 ** 256 - 1)
    print('Sdelan KEY:', pri_key)
    return pri_key



def create_public_key(n):
    pub_key = sympy.randprime(1, n)
    print('Sdelan public KEY:', pub_key)
    return pub_key


def create_part_key(my_pub_key, his_pub_key, my_private_key):
    his_pub_key = gmpy2.mpz(his_pub_key)
    my_pub_key = gmpy2.mpz(my_pub_key)
    my_private_key = gmpy2.mpz(my_private_key)
    part_key = gmpy2.powmod(his_pub_key, my_private_key, my_pub_key)

    print("Sdelan part_key:", part_key)
    return part_key


def create_full_key(his_part_key, my_private_key, his_public_key):
    his_part_key = gmpy2.mpz(his_part_key)
    my_private_key = gmpy2.mpz(my_private_key)
    his_public_key = gmpy2.mpz(his_public_key)
    full_key = gmpy2.powmod(his_part_key, my_private_key, his_public_key)
    return full_key


def encrypt_message(message, full_key):
    encrypted_message = ''
    key = gmpy2.mpz(full_key)
    for i in message:
        encrypted_message += chr(ord(i) + key)
    return encrypted_message


def decrypt_message(his_message, full_key):
    decrypted_message = ''
    key = gmpy2.mpz(full_key)
    for i in his_message:
        decrypted_message += chr(ord(i) - (key))
    return decrypted_message


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))


    private_key = create_private_key()
    public_key = create_public_key(private_key)
    client_socket.send(str(public_key).encode())
    print(f'Отправил свой открытый ключ - ', public_key)

    his_public_key = int(client_socket.recv(2048).decode())
    print('Принял его открытый ключ', his_public_key)


    my_part_key = create_part_key(public_key, his_public_key, private_key)
    print(f'Мой частичный ключ', my_part_key)
    client_socket.send(str(my_part_key).encode())

    his_part_key = int(client_socket.recv(2048).decode())
    print('Его частичный ключ - ', his_part_key)

    full_key = create_full_key(his_part_key, private_key, public_key)
    print('Full key - ', full_key)

    message = 'МЕНЯ ЗОВУТ АЛЕША! МЫ ДЕЛАЕМ ПРОТОКОЛ ДИФИ ХЕЛЛМАНА!'
    encrypted_message = encrypt_message(message, full_key)

    client_socket.send(str(encrypted_message).encode())

    his_encrypted_message = client_socket.recv(2048).decode()
    print('Получил зашифрованное сообщение - ', his_encrypted_message)

    print('Его сообщение:', decrypt_message(his_encrypted_message, full_key))
