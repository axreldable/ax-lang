import pytest
from ax_lang.interpreter.ax_lang import AxLang
from click.testing import CliRunner


@pytest.fixture
def ax_lang():
    return AxLang()


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()
