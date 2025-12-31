from tests.interpreter.test_utils import exec_test


def test_ax_lang(ax_lang):
    assert ax_lang.eval(1) == 1
    assert ax_lang.eval(42) == 42

    assert ax_lang.eval('"hello"') == "hello"


def test_ax_lang_eval(ax_lang):
    exec_test(ax_lang, "1", 1)
    exec_test(ax_lang, "-5.7", -5.7)
    exec_test(ax_lang, "(+ 1 -5.7)", -4.7)
    exec_test(ax_lang, "(+ -5.7 1)", -4.7)
