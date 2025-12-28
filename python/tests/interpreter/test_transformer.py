import pytest


class TestTransformer:
    def test_def_to_lambda(self, transformer):
        assert transformer.def_to_lambda(
            ["def", "add", ["x", "y"], ["+", "x", "y"]]
        ) == ["var", "add", ["lambda", ["x", "y"], ["+", "x", "y"]]]
        assert transformer.def_to_lambda(["def", "zero", [], 0]) == [
            "var",
            "zero",
            ["lambda", [], 0],
        ]

        body = ["begin", ["var", "x", 1], "x"]
        def_expr = ["def", "id", ["x"], body]
        assert transformer.def_to_lambda(def_expr) == [
            "var",
            "id",
            ["lambda", ["x"], body],
        ]

    def test_def_to_lambda_error(self, transformer):
        with pytest.raises(ValueError, match="not enough values to unpack"):
            # Not enough elements to unpack: _, name, params, body
            transformer.def_to_lambda(["def", "only_name"])

    def test_switch_to_if(self, transformer):
        assert transformer.switch_to_if(
            ["switch", [["==", "x", 10], 100], [[">", "x", 10], 200], ["else", 300]]
        ) == ["if", ["==", "x", 10], 100, ["if", [">", "x", 10], 200, 300]]

    def test_for_to_while(self, transformer):
        # Input: for loop expression
        # ['for', init, condition, modifier, body]
        for_expr = [
            "for",
            ["var", "counter", 0],
            ["<", "counter", 10],
            ["set", "counter", ["+", "counter", 1]],
            ["set", "rez", ["+", "rez", 2]],
        ]

        # Expected output: while loop expression
        # Structure: ['begin', init, ['while', condition, ['begin', body, modifier]]]
        expected = [
            "begin",
            ["var", "counter", 0],
            [
                "while",
                ["<", "counter", 10],
                [
                    "begin",
                    ["set", "rez", ["+", "rez", 2]],
                    ["set", "counter", ["+", "counter", 1]],
                ],
            ],
        ]

        result = transformer.for_to_while(for_expr)

        assert result == expected

    def test_inc_to_set(self, transformer):
        # Example: (++ x) -> (set x (+ x 1))
        expr = ["++", "x"]
        expected = ["set", "x", ["+", "x", 1]]
        assert transformer.inc_to_set(expr) == expected

    def test_dec_to_set(self, transformer):
        # Example: (-- y) -> (set y (- y 1))
        expr = ["--", "y"]
        expected = ["set", "y", ["-", "y", 1]]
        assert transformer.dec_to_set(expr) == expected

    def test_plus_assign_to_set(self, transformer):
        # Example: (+= count 5) -> (set count (+ count 5))
        expr = ["+=", "count", 5]
        expected = ["set", "count", ["+", "count", 5]]
        assert transformer.plus_assign_to_set(expr) == expected

    def test_minus_assign_to_set(self, transformer):
        # Example: (-= level 10) -> (set level (- level 10))
        expr = ["-=", "level", 10]
        expected = ["set", "level", ["-", "level", 10]]
        assert transformer.minus_assign_to_set(expr) == expected

    def test_multi_assign_to_set(self, transformer):
        # Example: (*= level 10) -> (set level (* level 10))
        expr = ["*=", "level", 10]
        expected = ["set", "level", ["*", "level", 10]]
        assert transformer.multi_assign_to_set(expr) == expected
