def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    i = 2
    prime = True
    while i * i <= n and prime:
        if n % i == 0:
            prime = False
        i += 1
    return prime


def count_primes(limit):
    count = 0
    i = 2
    while i <= limit:
        if is_prime(i):
            count += 1
        i += 1
    return count


count_primes(1000)
