import psutil
import sympy
import time

def prime_number():
    prime_number = sympy.randprime(2**127, 2**128 - 1)
    return prime_number * 4 + 3
def generate_e():
    p = prime_number()
    q = prime_number()
    M = p * q
    seed = psutil.cpu_stats()[0]
    for i in range(1):
        seed = pow(seed, 2) % M
        bit = bin(seed % 2)
    return bit[2:]
