def nested_loops(n):
    sum_val = 0
    i = 0
    while i < n:
        j = 0
        while j < n:
            sum_val += i + j
            j += 1
        i += 1
    return sum_val


nested_loops(100)
