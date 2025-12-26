from tests.interpreter.test_utils import exec_test


def test_blocks(ax_lang):
    assert (
        ax_lang.eval(
            ["begin", ["var", "x", 10], ["var", "y", 20], ["+", ["*", "x", "y"], 30]]
        )
        == 230
    )

    assert (
        ax_lang.eval(
            [
                "begin",
                ["var", "x", 10],
                [
                    "begin",
                    ["var", "x", 20],
                ],
                "x",
            ]
        )
        == 10
    )

    assert (
        ax_lang.eval(
            [
                "begin",
                ["var", "value", 10],
                ["var", "rez", ["begin", ["var", "x", ["+", "value", 10]], "x"]],
                "rez",
            ]
        )
        == 20
    )

    assert (
        ax_lang.eval(
            [
                "begin",
                ["var", "data", 10],
                [
                    "begin",
                    ["set", "data", 100],
                ],
                "data",
            ]
        )
        == 100
    )


def test_with_parser(ax_lang):
    exec_test(
        ax_lang,
        """
    ( begin
        (var x 10)
        (var y 20)
        (+ (* x 10) y)
    )
    """,
        120,
    )
