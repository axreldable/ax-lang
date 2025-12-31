import json
import logging
import re
import subprocess
from numbers import Number
from pathlib import Path
from typing import Optional

from ax_lang.exceptions import ParserError

logger = logging.getLogger(__name__)


EVA_GRAMMAR_PATH = str(Path(__file__).parent / "ax-lang-grammar.bnf.g")


def _get_parsed_value(syntax_cli_output: str) -> str:
    # Find the array that starts after "Parsed value:"
    after_parsed_value = syntax_cli_output.split("Parsed value:")[-1].strip()

    # Remove ANSI color codes (e.g. [22m)
    cleaned_parsed_value = re.sub(r"\x1B\[[0-9;]*[A-Za-z]", "", after_parsed_value)
    cleaned_parsed_value = cleaned_parsed_value.strip()
    return cleaned_parsed_value


def _try_parse_number(value: str) -> Optional[int | float]:
    value = value.strip()
    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        return None


def get_ast(expr: str) -> Number | str | list:
    # syntax-cli -g ax_lang/parser/ax-lang-grammar.bnf.g -m LALR1 -p 5
    logger.debug("Parsing expression...")
    logger.debug(f"Expression: `{expr}`.")

    # a hack to support negative numbers
    number = _try_parse_number(expr)
    if number is not None:
        return number

    result = subprocess.run(
        ["syntax-cli", "-g", EVA_GRAMMAR_PATH, "-m", "LALR1", "-p", expr],
        capture_output=True,
        text=True,  # decode bytes -> str automatically
    )
    if result.returncode != 0:
        raise ParserError(f"Failed to parse `{expr}`")

    output = result.stdout.strip()
    logger.debug(f"STDOUT: {output}")

    parsed_value = _get_parsed_value(output)
    logger.debug(f"parsed_value: {parsed_value}")

    try:
        data = json.loads(parsed_value)
    except json.JSONDecodeError:
        # Not valid JSON: treat as raw token/string (e.g. identifier)
        data = parsed_value
    except Exception as e:
        raise ParserError(f"Parser failed: {e}") from e

    return data
