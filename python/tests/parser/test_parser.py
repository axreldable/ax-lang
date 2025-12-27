from ax_lang.parser.parser import _get_parsed_value
from ax_lang.parser.parser import get_ast


def test_get_parsed_value():
    assert (
        _get_parsed_value(
            """
Parsing mode: LALR1_BY_SLR(1).

Parsing:

(begin ((lambda (x) (* x x)) 2))

✓ Accepted

Parsed value:

[
  "begin",
  [
    [
      "lambda",
      [
        "x"
      ],
      [
        "*",
        "x",
        "x"
      ]
    ],
    2
  ]
]
"""
        )
        == """[
  "begin",
  [
    [
      "lambda",
      [
        "x"
      ],
      [
        "*",
        "x",
        "x"
      ]
    ],
    2
  ]
]"""
    )


def test_get_parsed_value_x():
    assert _get_parsed_value("x") == "x"


def test_ast_functions():
    assert get_ast("(+ (+ 3 2) 5)") == ["+", ["+", 3, 2], 5]
    assert get_ast("((lambda (x) (* x x)) 2)") == [
        ["lambda", ["x"], ["*", "x", "x"]],
        2,
    ]
    assert (
        get_ast(
            """
        (def calc (x y)
            (begin
                (var z 30)
                (+ (* x y) z)
            ))
        """
        )
        == [
            "def",
            "calc",
            ["x", "y"],
            ["begin", ["var", "z", 30], ["+", ["*", "x", "y"], "z"]],
        ]
    )
    assert (
        get_ast(
            """
        (def factorial (x)
            (if (== x 1)
                1
                (* x (factorial (- x 1)))))
        """
        )
        == [
            "def",
            "factorial",
            ["x"],
            ["if", ["==", "x", 1], 1, ["*", "x", ["factorial", ["-", "x", 1]]]],
        ]
    )


def test_ast_classes():
    assert (
        get_ast(
            """
        (begin
            (class Point null
                (begin
                    (def constructor (this x y)
                        (begin
                            (set (prop this x) x)
                            (set (prop this y) y)))

                    (def calc (this)
                        (+ (prop this x) (prop this y)))
                )
            )

            (class Point3D Point
                (begin
                    (def constructor (this x y z)
                        (begin
                            ((prop (super Point3D) constructor) this x y)
                            (set (prop this z) z)))

                    (def calc (this)
                        (+ ((prop (super Point3D) calc) this)
                            (prop this z)))
                )
            )

            (var p (new Point3D 10 20 30))
            ((prop p calc) p)
        )
        """
        )
        == [
            "begin",
            [
                "class",
                "Point",
                "null",
                [
                    "begin",
                    [
                        "def",
                        "constructor",
                        ["this", "x", "y"],
                        [
                            "begin",
                            ["set", ["prop", "this", "x"], "x"],
                            ["set", ["prop", "this", "y"], "y"],
                        ],
                    ],
                    [
                        "def",
                        "calc",
                        ["this"],
                        ["+", ["prop", "this", "x"], ["prop", "this", "y"]],
                    ],
                ],
            ],
            [
                "class",
                "Point3D",
                "Point",
                [
                    "begin",
                    [
                        "def",
                        "constructor",
                        ["this", "x", "y", "z"],
                        [
                            "begin",
                            [
                                ["prop", ["super", "Point3D"], "constructor"],
                                "this",
                                "x",
                                "y",
                            ],
                            ["set", ["prop", "this", "z"], "z"],
                        ],
                    ],
                    [
                        "def",
                        "calc",
                        ["this"],
                        [
                            "+",
                            [["prop", ["super", "Point3D"], "calc"], "this"],
                            ["prop", "this", "z"],
                        ],
                    ],
                ],
            ],
            ["var", "p", ["new", "Point3D", 10, 20, 30]],
            [["prop", "p", "calc"], "p"],
        ]
    )


def test_ast_atoms():
    assert get_ast("1") == 1
    assert get_ast('"test"') == "test"
    assert get_ast("x") == "x"
