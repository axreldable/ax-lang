from ax_lang.interpreter.parser import get_lisp_representation


def test_parser(ax_lang):
    rez = get_lisp_representation("(begin (var x 10)(var y 20)(+ x y))")
    assert rez == ["begin", ["var", "x", 10], ["var", "y", 20], ["+", "x", "y"]]
