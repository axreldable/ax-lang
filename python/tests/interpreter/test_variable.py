import pytest


def test_variable(ax_lang):
    assert ax_lang.eval(["var", "x", 10]) == 10
    assert ax_lang.eval("x") == 10

    with pytest.raises(ValueError, match="is not defined"):
        ax_lang.eval("y")

    # default variables:
    assert ax_lang.eval("null") is None
    assert ax_lang.eval("true") is True
    assert ax_lang.eval("false") is False
    assert ax_lang.eval("VERSION") == "0.1.0"

    assert ax_lang.eval(["var", "is_user", "true"]) is True
    assert ax_lang.eval("is_user") is True

    assert ax_lang.eval(["var", "z", ["*", 3, 2]]) == 6
    assert ax_lang.eval("z") == 6
