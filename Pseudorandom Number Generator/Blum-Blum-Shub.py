import time
import psutil
import sys
from random import randint
from random import randrange

Start_time = time.time()

def is_prime(n, k=10):
    if n in [1, 2]:
        return True
    if n % 2 == 0:
        return False

    # Функция для разложения n-1 на степени двойки и нечетный множитель
    def decompose(n):
        s = 0
        while n % 2 == 0:
            s += 1
            n //= 2
        return s, n

    # Вычисляем s и d для n-1
    s, d = decompose(n - 1)

    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True



massiv = []
while len(massiv) < 2:
    num = randrange(2 ** 127, 2 ** 128 - 1)
    if is_prime(num) == True:
        massiv.append(num)

p, q = massiv[0], massiv[1]

v = psutil.virtual_memory()

print(f' число p = {p * 4 + 3}')
print(f' число q = {q * 4 + 3}')
M = p * q

count = 0

seed = int(v[1])
print(seed)


seed = (seed * seed) % M
with open('file.txt', 'w') as f:
    for i in range(0, 1500000):
        seed = pow(seed, 2) % M
        bit = str(seed % 2)
        f.write(bit + '')

print(f'Выполнено за {time.time() - Start_time} секунд.')
