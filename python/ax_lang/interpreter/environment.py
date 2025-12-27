import logging


logger = logging.getLogger(__name__)


class Environment:
    def __init__(self, record: dict, parent: "Environment" = None):
        self.record = record
        self.parent = parent

    def define(self, name, value):
        """Creates a variable with given name and value in the current Environment"""
        logger.debug(f"Defining name=`{name}` with value=`{value}` in the current env.")
        self.record[name] = value
        return value

    def assign(self, name, value):
        """Updates an existing variable."""
        name = str(name)  # in case need to assign ['prop', 'this', 'x']
        var_env = self.resolve(name)
        var_env.record[name] = value
        return value

    def lookup(self, name):
        """Returns the value of the variable
        or throws if it's not defined.
        """
        var_env = self.resolve(name)
        return var_env.record[name]

    def resolve(self, name) -> "Environment":
        """Returns the specific env in which the variable is defined.
        Throws if the variable is not defined.
        """
        name = str(name)  # in case need to resolve ['prop', 'this', 'x']
        if name in self.record:
            return self
        if not self.parent:
            raise ValueError(f"Variable `{name}` is not defined!")
        return self.parent.resolve(name)


class NativeFunctions:
    @staticmethod
    def minus(op1, op2=None):
        if op2 is None:
            return -op1
        return op1 - op2


def global_env() -> "Environment":
    env = Environment(
        {
            "null": None,
            "true": True,
            "false": False,
        }
    )
    # Math operations:
    env.define("+", lambda a, b: a + b)
    env.define("-", NativeFunctions.minus)
    env.define("*", lambda a, b: a * b)
    env.define("/", lambda a, b: a / b)
    # Comparison operations:
    env.define(">", lambda a, b: a > b)
    env.define(">=", lambda a, b: a >= b)
    env.define("<", lambda a, b: a < b)
    env.define("<=", lambda a, b: a <= b)
    env.define("==", lambda a, b: a == b)
    # print
    env.define("print", lambda *args: print(" ".join(args)))
    return env


GlobalEnvironment = global_env()
