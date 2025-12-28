def factorial_while(n):
    result = 1
    counter = n
    while counter > 0:
        result *= counter
        counter -= 1
    return result


def factorial_for(n):
    result = 1
    for i in range(n, 0, -1):
        result *= i
    return result


fact5_while = factorial_while(5)
fact5_for = factorial_for(5)
fact7 = factorial_while(7)

print(fact5_while, fact5_for, fact7)
print()
