import pytest
from ax_lang.interpreter.ax_lang import AxLang


@pytest.fixture
def ax_lang():
    return AxLang()
