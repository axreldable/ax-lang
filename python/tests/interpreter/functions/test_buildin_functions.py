from tests.interpreter.test_utils import exec_test


def test_add(ax_lang):
    exec_test(ax_lang, "(+ 1 5)", 6)
    exec_test(ax_lang, "(+ (+ 3 2) 5)", 10)


def test_sub(ax_lang):
    exec_test(ax_lang, "(- 1 5)", -4)
    exec_test(ax_lang, "(+ (- 3 2) 5)", 6)
    exec_test(ax_lang, "(- (- 3 2) 5)", -4)


def test_multi(ax_lang):
    exec_test(ax_lang, "(* 1 5)", 5)
    exec_test(ax_lang, "(* (* 3 2) 5)", 30)


def test_comparison(ax_lang):
    exec_test(ax_lang, "(> 1 5)", False)
    exec_test(ax_lang, "(< 1 5)", True)

    exec_test(ax_lang, "(>= 5 5)", True)
    exec_test(ax_lang, "(<= 5 5)", True)
    exec_test(ax_lang, "(== 5 5)", True)


def test_print(ax_lang):
    exec_test(ax_lang, '(print "Hello" "World")', None)
