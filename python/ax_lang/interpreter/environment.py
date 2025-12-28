import logging

from ax_lang.interpreter.functions import NativeFunctions

logger = logging.getLogger(__name__)


class Environment:
    """Manages variable scopes and bindings using a hierarchical environment chain.

    Each environment maintains a record of local bindings and a reference to its
    parent environment, enabling lexical scoping for variable resolution.
    """

    def __init__(self, record: dict, parent: "Environment" = None):
        """Create environment with local bindings and parent scope.

        Args:
            record: Dictionary of local variable bindings
            parent: Parent environment for scope chain (None for global scope)
        """
        self.record = record
        self.parent = parent

    def define(self, name, value):
        """Creates a variable with given name and value.

        Args:
            name: Variable name
            value: Variable value

        Returns:
            The value that was defined
        """
        logger.debug(f"Defining name=`{name}` with value=`{value}` in the current env.")
        self.record[name] = value
        return value

    def assign(self, name, value):
        """Updates an existing variable.

        Args:
            name: Variable name to update
            value: New value for the variable

        Returns:
            The value that was assigned

        Raises:
            ValueError: If the variable is not defined in this environment or any parent
        """
        name = str(name)  # in case need to assign ['prop', 'this', 'x']
        var_env = self.resolve(name)
        var_env.record[name] = value
        return value

    def lookup(self, name):
        """Returns the value of a variable.

        Args:
            name: Variable name to look up

        Returns:
            The value of the variable

        Raises:
            ValueError: If the variable is not defined in this environment or any parent
        """
        var_env = self.resolve(name)
        return var_env.record[name]

    def resolve(self, name) -> "Environment":
        """Returns the environment where variable is defined.

        Args:
            name: Variable name to resolve

        Returns:
            The environment containing the variable definition

        Raises:
            ValueError: If the variable is not defined in this environment or any parent
        """
        name = str(name)  # in case need to resolve ['prop', 'this', 'x']
        if name in self.record:
            return self
        if not self.parent:
            raise ValueError(f"Variable `{name}` is not defined!")
        return self.parent.resolve(name)


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
    env.define("print", NativeFunctions.print)
    return env


GlobalEnvironment = global_env()
