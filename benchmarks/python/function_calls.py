def simple_add(a, b):
    return a + b


def call_many_times(n):
    i = 0
    result = 0
    while i < n:
        result = simple_add(result, i)
        i += 1
    return result


call_many_times(10000)
