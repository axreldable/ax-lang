def factorial(n):
    result = 1
    counter = n
    while counter > 0:
        result *= counter
        counter -= 1
    return result


factorial(1000)
