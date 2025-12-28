def makeAdder(x):
    return lambda y: x + y


add5 = makeAdder(5)
add10 = makeAdder(10)

result1 = add5(3)
result2 = add10(3)


def apply(fn, x):
    return fn(x)


square = lambda x: x * x
result3 = apply(square, 4)


def compose(f, g):
    return lambda x: f(g(x))


double = lambda x: x * 2
increment = lambda x: x + 1

doubleThenIncrement = compose(increment, double)
result4 = doubleThenIncrement(5)

print(result1, result2, result3, result4)


def makeCounter():
    count = [0]  # Using list to maintain mutable state in closure

    def counter():
        count[0] = count[0] + 1
        return count[0]

    return counter


counter1 = makeCounter()
counter2 = makeCounter()

c1a = counter1()
c1b = counter1()
c2a = counter2()

print(c1a, c1b, c2a)
print()
