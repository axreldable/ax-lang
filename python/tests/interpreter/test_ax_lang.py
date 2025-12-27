import pytest


class TestAxLang:
    @pytest.mark.parametrize(
        "expr, is_name",
        [
            ("x", True),
            ("_x", True),
            ("x1", True),
            ("x_1", True),
            ("A", True),
            ("A_b2", True),
            ("", False),
            ("1x", False),
            ("a-b", False),
            ("a b", False),
            ("a.b", False),
            ("$", False),
            ("+", False),
            (
                "print",
                True,
            ),  # valid identifier, even if used as a native function elsewhere
            ('"x"', False),  # string literal form in this language, not an identifier
        ],
    )
    def test_is_variable_name(self, ax_lang, expr, is_name):
        assert ax_lang._is_variable_name(expr) is is_name
