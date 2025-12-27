class NativeFunctions:
    @staticmethod
    def minus(op1, op2=None):
        if op2 is None:
            return -op1
        return op1 - op2

    @staticmethod
    def print(*args):
        print(" ".join([str(arg) for arg in args]))
