import itertools
import math
import random


def main():
    print("Hello")
    n = get_semiprime(1000)
    print("semiprime N =", n)
    x, r, p, q = shors_algorithm_classical(n)
    print("semiprime N = ", n, ", coprime x = ", x, ", period r = ", r, ", prime factors = ", p, " and ", q, sep="")


def shors_algorithm_classical(n):
    x = random.randint(0, n)  # step one
    if math.gcd(x, n) != 1:  # step two
        return x, 0, math.gcd(x, n), n / math.gcd(x, n)
    r = find_period_classical(x, n)  # step three
    while r % 2 != 0:
        r = find_period_classical(x, n)
    p = math.gcd(x ** int(r / 2) + 1, n)  # step four, ignoring the case where (x^(r/2) +/- 1) is a multiple of N
    q = math.gcd(x ** int(r / 2) - 1, n)
    return x, r, p, q


# Sieve of Eratosthenes algorithm
def sieve():
    d = {}
    yield 2
    for q in itertools.islice(itertools.count(3), 0, None, 2):
        p = d.pop(q, None)
        if p is None:
            d[q * q] = q
            yield q
        else:
            x = p + q
            while x in d or not (x & 1):
                x += p
            d[x] = p


# Creates a list of prime numbers up to the given argument
def get_primes_sieve(n):
    return list(itertools.takewhile(lambda p: p < n, sieve()))


def get_semiprime(n):
    primes = get_primes_sieve(n)
    length = len(primes)
    p = primes[random.randrange(length)]
    q = primes[random.randrange(length)]
    return p * q


def find_period_classical(x, N):
    n = 1
    t = x
    while t != 1:
        t *= x
        t %= N
        n += 1
    return n


if __name__ == "__main__":
    main()
