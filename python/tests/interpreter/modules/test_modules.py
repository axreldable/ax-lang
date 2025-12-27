from tests.interpreter.test_utils import exec_test


def test_math(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (module math
            (begin
                (def abs (value)
                    (if (< value 0)
                        (- value)
                        value))

                (def square (x)
                    (* x x))

                (var MAX_VALUE 1000)
            )
        )

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
        (module math
            (begin
                (def abs (value)
                    (if (< value 0)
                        (- value)
                        value))

                (def square (x)
                    (* x x))

                (var MAX_VALUE 1000)
            )
        )

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
        (module math
            (begin
                (def abs (value)
                    (if (< value 0)
                        (- value)
                        value))

                (def square (x)
                    (* x x))

                (var MAX_VALUE 1000)
            )
        )

        (prop math MAX_VALUE)
    )
    """,
        1000,
    )
