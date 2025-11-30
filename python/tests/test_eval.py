def test_ax_lang(ax_lang):
    assert ax_lang.eval(1) == 1
    assert ax_lang.eval(42) == 42

    assert ax_lang.eval('"hello"') == "hello"
