import pytest
from ax_lang.interpreter.ax_lang import AxLang
from ax_lang.interpreter.transformer import Transformer


@pytest.fixture
def ax_lang():
    return AxLang()


@pytest.fixture()
def transformer():
    return Transformer()
