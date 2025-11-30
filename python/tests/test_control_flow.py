def test_if(ax_lang):
    assert (
        ax_lang.eval(
            [
                "begin",
                ["var", "x", 10],
                ["var", "y", 0],
                [
                    "if",
                    [">", "x", 10],
                    ["set", "y", 20],
                    ["set", "y", 30],
                ],
                "y",
            ]
        )
        == 30
    )


def test_while(ax_lang):
    assert (
        ax_lang.eval(
            [
                "begin",
                ["var", "counter", 0],
                ["var", "rez", 0],
                [
                    "while",
                    ["<", "counter", 10],
                    [
                        "begin",
                        ["set", "rez", ["+", "rez", 1]],
                        ["set", "counter", ["+", "counter", 1]],
                    ],
                ],
                "rez",
            ]
        )
        == 10
    )
