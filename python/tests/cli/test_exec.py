import tempfile
from pathlib import Path
from unittest.mock import patch

from ax_lang.cli.exec import cli
from ax_lang.cli.exec import eval_expression
from ax_lang.cli.exec import repl


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


class TestExprCommand:
    """Tests for the 'expr' command."""

    def test_expr_simple_expression(self, runner):
        """Test executing a simple expression."""
        result = runner.invoke(cli, ["expr", "(+ 2 3)"])
        assert result.exit_code == 0
        assert "5" in result.output

    def test_expr_lambda_function(self, runner):
        """Test executing a lambda function."""
        result = runner.invoke(cli, ["expr", "((lambda (x) (* x x)) 5)"])
        assert result.exit_code == 0
        assert "25" in result.output

    def test_expr_string_literal(self, runner):
        """Test executing a string expression."""
        result = runner.invoke(cli, ["expr", '"hello world"'])
        assert result.exit_code == 0
        assert "hello world" in result.output

    def test_expr_with_debug_flag(self, runner):
        """Test executing expression with debug flag."""
        result = runner.invoke(cli, ["expr", "(+ 1 1)", "--debug"])
        assert result.exit_code == 0
        assert "2" in result.output

    def test_expr_complex_expression(self, runner):
        """Test executing a complex expression with function definition."""
        expression = """(def calc (x y) (+ (* x y) 10)) (calc 3 4)"""
        result = runner.invoke(cli, ["expr", expression])
        assert result.exit_code == 0
        assert "22" in result.output

    def test_expr_nested_operations(self, runner):
        """Test executing nested arithmetic operations."""
        result = runner.invoke(cli, ["expr", "(+ (* 2 3) (- 10 5))"])
        assert result.exit_code == 0
        assert "11" in result.output


class TestFileCommand:
    """Tests for the 'file' command."""

    def test_file_simple_program(self, runner):
        """Test executing a simple ax-lang file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ax", delete=False) as f:
            f.write("(+ 10 20)")
            f.flush()
            filepath = f.name

        try:
            result = runner.invoke(cli, ["file", filepath])
            assert result.exit_code == 0
            assert "30" in result.output
        finally:
            Path(filepath).unlink()

    def test_file_with_variables(self, runner):
        """Test executing a file with variable declarations."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ax", delete=False) as f:
            f.write(
                """
                (var x 10)
                (var y 20)
                (+ x y)
                """
            )
            f.flush()
            filepath = f.name

        try:
            result = runner.invoke(cli, ["file", filepath])
            assert result.exit_code == 0
            assert "30" in result.output
        finally:
            Path(filepath).unlink()

    def test_file_with_function_definition(self, runner):
        """Test executing a file with function definition."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ax", delete=False) as f:
            f.write(
                """
                (def factorial (n)
                    (if (== n 1)
                        1
                        (* n (factorial (- n 1)))))
                (factorial 5)
                """
            )
            f.flush()
            filepath = f.name

        try:
            result = runner.invoke(cli, ["file", filepath])
            assert result.exit_code == 0
            assert "120" in result.output
        finally:
            Path(filepath).unlink()

    def test_file_nonexistent_file(self, runner):
        """Test executing a non-existent file."""
        result = runner.invoke(cli, ["file", "/nonexistent/file.ax"])
        assert result.exit_code != 0
        assert "Error" in result.output or "does not exist" in result.output.lower()

    def test_file_with_class(self, runner):
        """Test executing a file with class definition."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ax", delete=False) as f:
            f.write(
                """
                (class Point null
                    (begin
                        (def constructor (this x y)
                            (begin
                                (set (prop this x) x)
                                (set (prop this y) y)))
                        (def calc (this)
                            (+ (prop this x) (prop this y)))
                    ))
                (var p (new Point 10 20))
                ((prop p calc) p)
                """
            )
            f.flush()
            filepath = f.name

        try:
            result = runner.invoke(cli, ["file", filepath])
            assert result.exit_code == 0
            assert "30" in result.output
        finally:
            Path(filepath).unlink()


class TestRepl:
    """Tests for the REPL functionality."""

    def assert_calls_no_errors(self, calls: list) -> None:
        for call in calls:
            assert "error" not in str(call).lower()

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_exit_command(self, mock_echo, mock_input):
        """Test REPL exits on 'exit' command."""
        mock_input.side_effect = ["exit"]

        repl()

        mock_input.assert_called_once()
        # Verify "Goodbye!" was printed
        calls = [str(call) for call in mock_echo.call_args_list]
        self.assert_calls_no_errors(calls)
        assert any("Goodbye!" in str(call) for call in calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_quit_command(self, mock_echo, mock_input):
        """Test REPL exits on 'quit' command."""
        mock_input.side_effect = ["quit"]

        repl()

        mock_input.assert_called_once()
        calls = [str(call) for call in mock_echo.call_args_list]
        self.assert_calls_no_errors(calls)
        assert any("Goodbye!" in str(call) for call in calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_simple_expression(self, mock_echo, mock_input):
        """Test REPL evaluates simple expressions."""
        mock_input.side_effect = ["(+ 1 2)", "exit"]

        repl()

        # Find the call where 3 was echoed (result of 1+2)
        calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        self.assert_calls_no_errors(calls)
        assert 3 in calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_variable_persistence(self, mock_echo, mock_input):
        """Test REPL maintains variable state across inputs."""
        mock_input.side_effect = ["(var x 10)", "x", "(+ x 5)", "exit"]

        repl()

        # Check that variable value persists
        calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        # self.assert_calls_no_errors(calls)
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
        self.assert_calls_no_errors(calls)
        assert 2 in calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_eof_error(self, mock_echo, mock_input):
        """Test REPL handles EOF (Ctrl+D) gracefully."""
        mock_input.side_effect = EOFError()

        repl()

        calls = [str(call) for call in mock_echo.call_args_list]
        self.assert_calls_no_errors(calls)
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
        self.assert_calls_no_errors(calls)
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
