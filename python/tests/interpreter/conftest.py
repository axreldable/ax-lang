import pytest
from ax_lang.interpreter.ax_lang import AxLang
from ax_lang.interpreter.ax_lang import GlobalEnvironment


@pytest.fixture
def ax_lang():
    return AxLang(GlobalEnvironment)
