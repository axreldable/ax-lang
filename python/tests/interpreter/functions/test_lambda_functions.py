from tests.interpreter.test_utils import exec_test


def test_simple_lambda(ax_lang):
    # (lambda x: x * 2)(2)
    exec_test(
        ax_lang,
        """
    ((lambda (x) (* x x)) 2)
    """,
        4,
    )


def test_lambda_variable(ax_lang):
    # square = lambda x: x * x
    # square(2)
    exec_test(
        ax_lang,
        """
    (begin
        (var square (lambda (x) (* x x)))
        (square 2))
    """,
        4,
    )


def test_on_click(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (def onClick (callback)
        (begin
            (var x 10)
            (var y 20)
            (callback (+ x y))
        ))

        (onClick (lambda (data) (* data 10)))
    )
    """,
        300,
    )
