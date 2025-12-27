from ax_lang.parser.parser import get_ast


def test_parser(ax_lang):
    rez = get_ast("(begin (var x 10)(var y 20)(+ x y))")
    assert rez == ["begin", ["var", "x", 10], ["var", "y", 20], ["+", "x", "y"]]
