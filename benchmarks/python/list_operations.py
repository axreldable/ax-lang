def sum_list(lst):
    sum_val = 0
    i = 0
    length = len(lst)
    while i < length:
        sum_val += lst[i]
        i += 1
    return sum_val


def create_and_sum(n):
    lst = []
    i = 0
    while i < n:
        lst.append(i)
        i += 1
    return sum_list(lst)


create_and_sum(1000)
