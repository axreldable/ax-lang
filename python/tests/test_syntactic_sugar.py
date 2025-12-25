from tests.test_utils import exec_test


def test_switch(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (var x 10)

        (switch
            ((== x 10) 100)
            ((> x 10) 200)
            (else 300)
        )
    )
    """,
        100,
    )


def test_for(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (var counter 0)
        (var rez 0)

        (while (< counter 10)
        (begin
            (set rez (+ rez 2))
            (set counter (+ counter 1))
        ))

        rez
    )
    """,
        20,
    )

    exec_test(
        ax_lang,
        """
    (begin
        (var counter 0)
        (var rez 0)

        (for (var counter 0) (< counter 10) (set counter (+ counter 1))
            (set rez (+ rez 2)))

        rez
    )
    """,
        20,
    )


def test_unary(ax_lang):
    exec_test(
        ax_lang,
        """
        (begin
            (var v 1)
            (++ v)
            (++ v)
        )
    """,
        3,
    )

    exec_test(
        ax_lang,
        """
        (begin
            (var v 10)
            (-- v)
            (-- v)
        )
    """,
        8,
    )

    exec_test(
        ax_lang,
        """
        (begin
            (var v 10)
            (+= v 5)
            v
        )
    """,
        15,
    )

    exec_test(
        ax_lang,
        """
        (begin
            (var v 10)
            (-= v 5)
            v
        )
    """,
        5,
    )
