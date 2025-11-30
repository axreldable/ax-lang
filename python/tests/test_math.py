def test_add(ax_lang):
    assert ax_lang.eval(["+", 1, 5]) == 6
    assert ax_lang.eval(["+", ["+", 3, 2], 5]) == 10


def test_sub(ax_lang):
    assert ax_lang.eval(["-", 1, 5]) == -4
    assert ax_lang.eval(["+", ["-", 3, 2], 5]) == 6
    assert ax_lang.eval(["-", ["-", 3, 2], 5]) == -4


def test_multi(ax_lang):
    assert ax_lang.eval(["*", 1, 5]) == 5
    assert ax_lang.eval(["*", ["*", 3, 2], 5]) == 30
