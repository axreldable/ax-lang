from ax_lang.interpreter.parser import get_lisp_representation


def exec_test(ax_lang, code, expected):
    expr = get_lisp_representation(code)
    assert ax_lang.eval(expr) == expected
