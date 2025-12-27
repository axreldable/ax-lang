import logging


logger = logging.getLogger(__name__)


class Transformer:
    """Performs Just-In-Time transformations of syntactic sugar into core language constructs.

    The transformer converts high-level syntactic constructs into simpler, equivalent
    expressions that the interpreter can directly evaluate.
    """

    def def_to_lambda(self, def_expr: list) -> list:
        """Transforms function definition to lambda.

        Translates a function declaration into a variable declaration with a lambda expression.

        Args:
            def_expr: Function definition in the form ["def", name, params, body]

        Returns:
            Variable declaration in the form ["var", name, ["lambda", params, body]]

        Example:
            ["def", "square", ["x"], ["*", "x", "x"]]
            -> ["var", "square", ["lambda", ["x"], ["*", "x", "x"]]]
        """
        _, name, params, body = def_expr
        return ["var", name, ["lambda", params, body]]

    def switch_to_if(self, switch_expr: list) -> list:
        """Transforms switch to nested if expressions.

        Converts a switch statement into a chain of nested if-else expressions.

        Args:
            switch_expr: Switch expression with cases

        Returns:
            Nested if expression

        Example:
            ["switch", [["==", "x", 10], 100], [[">", "x", 10], 200], ["else", 300]]
            -> ["if", ["==", "x", 10], 100, ["if", [">", "x", 10], 200, 300]]
        """
        logger.debug(f"Transforming switch expr=`{switch_expr}`...")
        _, *cases = switch_expr
        if_expr = ["if", None, None, None]
        curr_if = if_expr
        for i in range(len(cases) - 1):
            curr_cond, curr_block = cases[i]
            curr_if[1] = curr_cond
            curr_if[2] = curr_block

            next_cond, next_block = cases[i + 1]
            curr_if[3] = next_block if next_cond == "else" else ["if", None, None, None]

            curr_if = curr_if[3]
        logger.debug(f"Result if expr=`{if_expr}`.")
        return if_expr

    def for_to_while(self, for_expr: list) -> list:
        """Transforms for-loop to while-loop.

        Converts a for-loop into an equivalent while-loop with initialization.

        Args:
            for_expr: For-loop in the form ["for", init, condition, modifier, body]

        Returns:
            While-loop in the form ["begin", init, ["while", condition, ["begin", body, modifier]]]

        Example:
            ["for", ["var", "i", 0], ["<", "i", 10], ["set", "i", ["+", "i", 1]], ["print", "i"]]
            -> ["begin", ["var", "i", 0],
                ["while", ["<", "i", 10], ["begin", ["print", "i"], ["set", "i", ["+", "i", 1]]]]]
        """
        logger.debug(f"Transforming `for` expr=`{for_expr}`...")
        _, init, condition, modifier, body = for_expr
        while_expr = [
            "begin",
            init,
            ["while", condition, ["begin", body, modifier]],
        ]
        logger.debug(f"Result `while` expr=`{while_expr}`.")
        return while_expr

    def inc_to_set(self, expr: list) -> list:
        """Transforms ++ to set expression.

        Args:
            expr: Increment expression ["++", var]

        Returns:
            Set expression ["set", var, ["+", var, 1]]

        Example:
            ["++", "x"] -> ["set", "x", ["+", "x", 1]]
        """
        _, var = expr
        set_expr = ["set", var, ["+", var, 1]]
        return set_expr

    def dec_to_set(self, expr: list) -> list:
        """Transforms -- to set expression.

        Args:
            expr: Decrement expression ["--", var]

        Returns:
            Set expression ["set", var, ["-", var, 1]]

        Example:
            ["--", "y"] -> ["set", "y", ["-", "y", 1]]
        """
        _, var = expr
        set_expr = ["set", var, ["-", var, 1]]
        return set_expr

    def plus_assign_to_set(self, expr: list) -> list:
        """Transforms += to set expression.

        Args:
            expr: Plus-assign expression ["+=", var, value]

        Returns:
            Set expression ["set", var, ["+", var, value]]

        Example:
            ["+=", "count", 5] -> ["set", "count", ["+", "count", 5]]
        """
        _, var, value = expr
        set_expr = ["set", var, ["+", var, value]]
        return set_expr

    def minus_assign_to_set(self, expr: list) -> list:
        """Transforms -= to set expression.

        Args:
            expr: Minus-assign expression ["-=", var, value]

        Returns:
            Set expression ["set", var, ["-", var, value]]

        Example:
            ["-=", "level", 10] -> ["set", "level", ["-", "level", 10]]
        """
        _, var, value = expr
        set_expr = ["set", var, ["-", var, value]]
        return set_expr
