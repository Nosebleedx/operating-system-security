import time
import psutil
from random import randint
from random import randrange

Start_time = time.time()

def salt():
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
    p = p * 4 + 3
    q = q * 4 + 3
    M = p * q



    seed = int(v[1])
    seed = (seed * seed) % M
    bits = []
    for i in range(0, 256):
        seed = pow(seed, 2) % M
        bit = bin(seed % 2)
        bits.append(bit[2:])

    bbs = ''
    for i in range(len(bits)):
        bbs += bits[i]
    bit_end = bytearray(bbs.encode())
    return bit_end

