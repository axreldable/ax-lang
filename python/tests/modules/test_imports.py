from tests.test_utils import exec_test


def test_math(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (import math)
        ((prop math abs) (- 10))
    )
    """,
        10,
    )


def test_math_func(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (import math)
        (var abs (prop math abs))
        (abs (- 10))
    )
    """,
        10,
    )


def test_max_value(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (import math)
        (prop math MAX_VALUE)
    )
    """,
        1000,
    )
