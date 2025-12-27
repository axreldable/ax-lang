import logging


logger = logging.getLogger(__name__)


class Transformer:
    def def_to_lambda(self, def_expr):
        """Translates `def`-expression (function declaration) into a variable declaration with a lambda expression."""
        _, name, params, body = def_expr
        return ["var", name, ["lambda", params, body]]

    def switch_to_if(self, switch_expr):
        """
        Example:
            Transforming switch expr=`['switch', [['==', 'x', 10], 100], [['>', 'x', 10], 200], ['else', 300]]`...
            Result if expr=`['if', ['==', 'x', 10], 100, ['if', ['>', 'x', 10], 200, 300]]`.
        """
        # ['switch', [['=', 'x', 10], 100], [['>', 'x', 10], 200], ['else', 300]]
        # ['if', ['==', 'x', 10], 100, ['if', ['>', 'x', 10], 200, 300]]
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

    def for_to_while(self, for_expr):
        """
        Transforming `for` expr=`['for', ['var', 'counter', 0], ['<', 'counter', 10],
            ['set', 'counter', ['+', 'counter', 1]], ['set', 'rez', ['+', 'rez', 2]]]`...
        Result `while` expr=`['begin', ['var', 'counter', 0], ['while', ['<', 'counter', 10],
            ['begin', ['set', 'rez', ['+', 'rez', 2]], ['set', 'counter', ['+', 'counter', 1]]]]]`.
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

    def inc_to_set(self, expr):
        """Example: (++ x) -> (set x (+ x 1))."""
        _, var = expr
        set_expr = ["set", var, ["+", var, 1]]
        return set_expr

    def dec_to_set(self, expr):
        """Example: (-- y) -> (set y (- y 1))."""
        _, var = expr
        set_expr = ["set", var, ["-", var, 1]]
        return set_expr

    def plus_assign_to_set(self, expr):
        """Example: (+= count 5) -> (set count (+ count 5))."""
        _, var, value = expr
        set_expr = ["set", var, ["+", var, value]]
        return set_expr

    def minus_assign_to_set(self, expr):
        """Example: (-= level 10) -> (set level (- level 10))"""
        _, var, value = expr
        set_expr = ["set", var, ["-", var, value]]
        return set_expr
