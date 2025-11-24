import json
import logging
import re
import subprocess


logger = logging.getLogger(__name__)


EVA_GRAMMAR_PATH = "ax_lang/interpreter/parser/ax-lang-grammar.bnf.g"


def _get_parsed_value(syntax_cli_output: str) -> str:
    # Find the array that starts after "Parsed value:"
    after_parsed_value = syntax_cli_output.split("Parsed value:")[-1].strip()

    # Remove ANSI color codes (e.g. [22m)
    cleaned_parsed_value = re.sub(r"\x1B\[[0-9;]*[A-Za-z]", "", after_parsed_value)
    return cleaned_parsed_value


def get_lisp_representation(expr: str):
    result = subprocess.run(
        ["syntax-cli", "-g", EVA_GRAMMAR_PATH, "-m", "LALR1", "-p", expr],
        capture_output=True,
        text=True,  # decode bytes -> str automatically
        check=True,  # raise error if return code != 0
    )

    output = result.stdout.strip()
    logger.debug(f"STDOUT: {output}")

    parsed_value = _get_parsed_value(output)
    logger.debug(f"parsed_value: {parsed_value}")
    data = json.loads(parsed_value)
    return data
