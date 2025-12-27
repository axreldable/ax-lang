def test_print_str(ax_lang, capsys):
    assert ax_lang.eval(["print", '"hello"', '"world"']) is None
    out = capsys.readouterr().out
    assert out == "hello world\n"


def test_print_number(ax_lang, capsys):
    assert ax_lang.eval(["print", 1, 2]) is None
    out = capsys.readouterr().out
    assert out == "1 2\n"
