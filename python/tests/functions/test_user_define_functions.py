from tests.test_utils import exec_test


def test_simple_udf(ax_lang):
    """
    >>> def square(x):
    ...     return x * x
    >>>
    >>> square(2)
    """
    exec_test(
        ax_lang,
        """
    (begin
        (def square (x)
            (* x x))

        (square 2)
    )
    """,
        4,
    )


def test_udf_with_body(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (def square (x)
        (begin
            (* x x)
        ))

        (square 2)
    )
    """,
        4,
    )


def test_closures(ax_lang):
    """
    >>> x = 10
    >>> def foo():
    ...     return x
    >>>
    >>> def bar():
    ...     x = 20
    ...     return foo() + x
    >>>
    >>> bar()
    """
    exec_test(
        ax_lang,
        """
    (begin
        (var x 10)

        (def foo () x)

        (def bar ()
        (begin
            (var x 20)
            (+ (foo) x)
        ))

        (bar)
    )
    """,
        30,
    )


def test_udf_with_complex_body(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (def calc (x y)
        (begin
            (var z 30)
            (+ (* x y) z)
        ))

        (calc 10 20)
    )
    """,
        230,
    )


def test_on_click(ax_lang):
    """
    >>> def onClick(callback):
    ...     x = 10
    ...     y = 20
    ...     return callback(x + y)
    ...
    >>> def multy(x):
    ...     return x * 10
    ...
    >>> onClick(multy)
    """
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

        (def multy (x)
            (* x 10))

        (onClick multy)
    )
    """,
        300,
    )


def test_wrappers(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (var value 100)

        (def calc (x y)
        (begin
            (var z (+ x y))

            (def inner (foo)
                (+ (+ foo z) value))

            inner
        ))

        (var fn (calc 10 20))

        (fn 30)
    )
    """,
        160,
    )
