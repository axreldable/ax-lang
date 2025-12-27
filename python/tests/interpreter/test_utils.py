from ax_lang.parser.parser import get_ast


def exec_test(ax_lang, code, expected):
    expr = get_ast(code)
    assert ax_lang.eval(expr) == expected
