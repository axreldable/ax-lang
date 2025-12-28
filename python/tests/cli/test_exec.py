import tempfile
from pathlib import Path
from unittest.mock import patch

from ax_lang.cli.exec import cli, eval_expression, repl
from click.testing import CliRunner
from tests.cli.common import assert_calls_no_errors


class TestEvalExpr:
    """Tests for the eval_expression function."""

    def test_eval_expression_simple_expression(self, ax_lang):
        """Test evaluating a simple arithmetic expression."""
        result = eval_expression(ax_lang, "(+ 1 2)")
        assert result == 3

    def test_eval_expression_variable_declaration(self, ax_lang):
        """Test evaluating variable declaration."""
        result = eval_expression(ax_lang, "(var x 10) x")
        assert result == 10

    def test_eval_expression_multiple_expressions(self, ax_lang):
        """Test evaluating multiple expressions in sequence."""
        result = eval_expression(
            ax_lang,
            """
            (var x 5)
            (var y 10)
            (+ x y)
            """,
        )
        assert result == 15

    def test_eval_expression_function_definition(self, ax_lang):
        """Test evaluating function definition and invocation."""
        result = eval_expression(
            ax_lang,
            """
            (def square (x) (* x x))
            (square 4)
            """,
        )
        assert result == 16


runner = CliRunner()


def cli_output(args):
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    return result.output.strip()


def cli_error_output(args):
    result = runner.invoke(cli, args)
    assert result.exit_code != 0
    return result.output.strip()


class TestExprCommand:
    """Tests for the 'expr' command."""

    def test_cli_expr(self):
        assert cli_output(["expr", "(+ 2 3)"]) == "5"
        assert cli_output(["expr", "((lambda (x) (* x x)) 5)"]) == "25"
        assert cli_output(["expr", '"hello world"']) == "hello world"
        assert (
            cli_output(["expr", "(def calc (x y) (+ (* x y) 10)) (calc 3 4)"]) == "22"
        )
        assert cli_output(["expr", "(+ (* 2 3) (- 10 5))"]) == "11"

    def test_cli_expr_debug(self):
        assert cli_output(["expr", "(+ 1 1)", "--debug"]) == "2"


class TestFileCommand:
    def cli_file_output(self, file_content):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ax", delete=False) as tmp:
            tmp.write(file_content)
            tmp.flush()
            filepath = tmp.name
        try:
            result = cli_output(["file", filepath])
            return result
        finally:
            Path(filepath).unlink()

    def test_cli_file(self):
        assert self.cli_file_output("(+ 10 20)") == "30"
        assert (
            self.cli_file_output(
                """
                (var x 10)
                (var y 20)
                (+ x y)
                """
            )
            == "30"
        )

    def test_cli_file_nonexistent_file(self):
        rez = cli_error_output(["file", "/nonexistent/file.ax"])
        assert "Error" in rez
        assert "does not exist" in rez


class TestRepl:
    """Tests for the REPL functionality."""

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_exit_command(self, mock_echo, mock_input):
        """Test REPL exits on 'exit' command."""
        mock_input.side_effect = ["exit"]

        repl()

        mock_input.assert_called_once()
        # Verify "Goodbye!" was printed
        calls = [str(call) for call in mock_echo.call_args_list]
        assert_calls_no_errors(calls)
        assert any("Goodbye!" in str(call) for call in calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_quit_command(self, mock_echo, mock_input):
        """Test REPL exits on 'quit' command."""
        mock_input.side_effect = ["quit"]

        repl()

        mock_input.assert_called_once()
        calls = [str(call) for call in mock_echo.call_args_list]
        assert_calls_no_errors(calls)
        assert any("Goodbye!" in str(call) for call in calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_simple_expression(self, mock_echo, mock_input):
        """Test REPL evaluates simple expressions."""
        mock_input.side_effect = ["(+ 1 2)", "exit"]

        repl()

        # Find the call where 3 was echoed (result of 1+2)
        calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert_calls_no_errors(calls)
        assert 3 in calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_variable_persistence(self, mock_echo, mock_input):
        """Test REPL maintains variable state across inputs."""
        mock_input.side_effect = ["(var x 10)", "x", "(+ x 5)", "exit"]

        repl()

        # Check that variable value persists
        calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert_calls_no_errors(calls)
        assert 10 in calls  # First x evaluation
        assert 15 in calls  # x + 5 evaluation

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_empty_input(self, mock_echo, mock_input):
        """Test REPL handles empty input gracefully."""
        mock_input.side_effect = ["", "   ", "(+ 1 1)", "exit"]

        repl()

        # Should evaluate (+ 1 1) = 2
        calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert_calls_no_errors(calls)
        assert 2 in calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_eof_error(self, mock_echo, mock_input):
        """Test REPL handles EOF (Ctrl+D) gracefully."""
        mock_input.side_effect = EOFError()

        repl()

        calls = [str(call) for call in mock_echo.call_args_list]
        assert_calls_no_errors(calls)
        assert any("Goodbye!" in str(call) for call in calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_keyboard_interrupt(self, mock_echo, mock_input):
        """Test REPL handles KeyboardInterrupt (Ctrl+C) gracefully."""
        mock_input.side_effect = [KeyboardInterrupt(), "exit"]

        repl()

        # Should show message about using exit/quit
        output = [str(call) for call in mock_echo.call_args_list]
        assert any("exit" in str(call).lower() for call in output)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_evaluation_error(self, mock_echo, mock_input):
        """Test REPL handles evaluation errors gracefully."""
        mock_input.side_effect = ["(undefined_var)", "exit"]

        repl()

        # Should print error message
        calls = [str(call) for call in mock_echo.call_args_list]
        assert any("Error" in str(call) for call in calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_function_definition(self, mock_echo, mock_input):
        """Test REPL can define and use functions."""
        mock_input.side_effect = [
            "(def square (x) (* x x))",
            "(square 4)",
            "exit",
        ]

        repl()

        calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert_calls_no_errors(calls)
        assert 16 in calls


class TestCliGroup:
    """Tests for the CLI group (main entry point)."""

    def test_cli_no_command_starts_repl(self, runner):
        """Test that running CLI without command starts REPL."""
        # Invoke with no subcommand and provide input to exit immediately
        result = runner.invoke(cli, [], input="exit\n")
        assert "AxLang Interactive Interpreter" in result.output
        assert "Goodbye!" in result.output

    def test_cli_help(self, runner):
        """Test CLI help output."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "AxLang interpreter" in result.output
        assert "expr" in result.output
        assert "file" in result.output

    def test_expr_command_help(self, runner):
        """Test expr command help output."""
        result = runner.invoke(cli, ["expr", "--help"])
        assert result.exit_code == 0
        assert "Execute an AxLang expression" in result.output
        assert "--debug" in result.output

    def test_file_command_help(self, runner):
        """Test file command help output."""
        result = runner.invoke(cli, ["file", "--help"])
        assert result.exit_code == 0
        assert "Execute an AxLang file" in result.output
        assert "FILEPATH" in result.output
