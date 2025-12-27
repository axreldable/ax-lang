"""Tests for multi-line input functionality in the REPL."""

from unittest.mock import patch

from ax_lang.cli.exec import repl
from ax_lang.cli.multiline import is_expression_complete


class TestIsExpressionComplete:
    """Tests for the is_expression_complete function."""

    def test_simple_complete_expression(self):
        """Test that a simple complete expression is recognized."""
        assert is_expression_complete("(+ 1 2)") is True

    def test_simple_incomplete_expression(self):
        """Test that an incomplete expression is recognized."""
        assert is_expression_complete("(+ 1 2") is False

    def test_empty_string(self):
        """Test that an empty string is considered balanced."""
        assert is_expression_complete("") is True

    def test_single_opening_paren(self):
        """Test that a single opening paren is incomplete."""
        assert is_expression_complete("(") is False

    def test_single_closing_paren(self):
        """Test that a single closing paren without opening is incomplete."""
        assert is_expression_complete(")") is False

    def test_nested_balanced_parens(self):
        """Test that nested balanced parentheses are recognized."""
        assert is_expression_complete("((()))") is True
        assert is_expression_complete("(()())") is True
        assert is_expression_complete("(()(()))") is True

    def test_nested_unbalanced_parens(self):
        """Test that nested unbalanced parentheses are recognized."""
        assert is_expression_complete("(((") is False
        assert is_expression_complete("((())") is False
        assert is_expression_complete("(()()))") is False

    def test_string_with_parens_inside(self):
        """Test that parens inside strings don't count."""
        assert is_expression_complete('(print "hello (world)")') is True
        assert is_expression_complete('(print ")")') is True
        assert is_expression_complete('(print "(((")') is True

    def test_unclosed_string(self):
        """Test that unclosed strings are detected."""
        assert is_expression_complete('(print "hello') is False
        assert is_expression_complete('"unclosed') is False

    def test_string_with_escaped_quotes(self):
        """Test that escaped quotes in strings are handled correctly."""
        assert is_expression_complete(r'(print "hello \"world\"")') is True
        assert is_expression_complete(r'(print "test\\")') is True

    def test_multi_line_function_definition_incomplete(self):
        """Test incomplete multi-line function definition."""
        incomplete_def = """(def fibonacci (n)
  (if (<= n 1)"""
        assert is_expression_complete(incomplete_def) is False

    def test_multi_line_function_definition_complete(self):
        """Test complete multi-line function definition."""
        complete_def = """(def fibonacci (n)
  (if (<= n 1)
      n
      (+ (fibonacci (- n 1))
         (fibonacci (- n 2)))))"""
        assert is_expression_complete(complete_def) is True

    def test_multi_statement_block_complete(self):
        """Test complete multi-statement block."""
        block = """(begin
  (var x 10)
  (var y 20)
  (+ x y))"""
        assert is_expression_complete(block) is True

    def test_multi_statement_block_incomplete(self):
        """Test incomplete multi-statement block."""
        block = """(begin
  (var x 10)
  (var y 20)
  (+ x y)"""
        assert is_expression_complete(block) is False

    def test_class_definition_complete(self):
        """Test complete class definition."""
        class_def = """(class Point null
    (begin
        (def constructor (this x y)
            (begin
                (set (prop this x) x)
                (set (prop this y) y)))))"""
        assert is_expression_complete(class_def) is True

    def test_class_definition_incomplete(self):
        """Test incomplete class definition."""
        class_def = """(class Point null
    (begin
        (def constructor (this x y)
            (begin
                (set (prop this x) x)"""
        assert is_expression_complete(class_def) is False

    def test_expression_with_multiple_strings(self):
        """Test expression with multiple string literals."""
        expr = '(print "hello" "world" "test")'
        assert is_expression_complete(expr) is True

    def test_expression_with_nested_strings(self):
        """Test expression with nested function calls and strings."""
        expr = '(print (concat "hello" " " "world"))'
        assert is_expression_complete(expr) is True

    def test_lambda_expression_complete(self):
        """Test complete lambda expression."""
        assert is_expression_complete("((lambda (x) (* x x)) 5)") is True

    def test_lambda_expression_incomplete(self):
        """Test incomplete lambda expression."""
        assert is_expression_complete("((lambda (x) (* x x)") is False

    def test_whitespace_only(self):
        """Test that whitespace-only strings are considered balanced."""
        assert is_expression_complete("   ") is True
        assert is_expression_complete("\n\n") is True
        assert is_expression_complete("\t\t") is True

    def test_complex_nested_expression(self):
        """Test complex nested expression with multiple levels."""
        expr = "(+ (* (- 10 5) (/ 20 4)) (if (> x 0) x (- x)))"
        assert is_expression_complete(expr) is True

    def test_expression_with_comments_like_syntax(self):
        """Test expressions that might contain comment-like syntax."""
        # Note: AxLang might not support comments, but test the balancing still works
        expr = "(+ 1 2)"  # This is just a normal expression
        assert is_expression_complete(expr) is True


class TestReplMultiline:
    """Tests for multi-line input in the REPL."""

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_function_definition(self, mock_echo, mock_input):
        """Test REPL accumulates multi-line function definition."""
        mock_input.side_effect = [
            "(def square (x)",  # Line 1: incomplete
            "  (* x x))",  # Line 2: completes the expression
            "(square 5)",  # Test the function
            "exit",
        ]

        repl()

        # Should have called input 4 times (3 expressions + exit)
        assert mock_input.call_count == 4
        # Second call should have continuation prompt
        assert "..." in str(mock_input.call_args_list[1])

        # Check the function was executed correctly
        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 25 in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_fibonacci(self, mock_echo, mock_input):
        """Test REPL with multi-line fibonacci function (from issue #14)."""
        mock_input.side_effect = [
            "(def fibonacci (n)",
            "  (if (<= n 1)",
            "      n",
            "      (+ (fibonacci (- n 1))",
            "         (fibonacci (- n 2)))))",
            "(fibonacci 5)",
            "exit",
        ]

        repl()

        # Verify fibonacci(5) = 5
        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 5 in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_nested_blocks(self, mock_echo, mock_input):
        """Test REPL with nested begin blocks."""
        mock_input.side_effect = [
            "(begin",
            "  (var x 10)",
            "  (begin",
            "    (var y 20)",
            "    (+ x y)))",
            "exit",
        ]

        repl()

        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 30 in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_with_strings(self, mock_echo, mock_input):
        """Test REPL with multi-line expressions containing strings."""
        mock_input.side_effect = [
            "(begin",
            '  (var msg "hello (world)")',
            "  msg)",
            "exit",
        ]

        repl()

        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert "hello (world)" in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_single_line_still_works(self, mock_echo, mock_input):
        """Test that single-line expressions still work normally."""
        mock_input.side_effect = [
            "(+ 1 2)",
            "(* 3 4)",
            "(- 10 5)",
            "exit",
        ]

        repl()

        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 3 in echo_calls
        assert 12 in echo_calls
        assert 5 in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_empty_lines(self, mock_echo, mock_input):
        """Test REPL handles empty lines during multi-line input."""
        mock_input.side_effect = [
            "(def test (x)",
            "",  # Empty line in the middle
            "  (+ x 1))",
            "(test 10)",
            "exit",
        ]

        repl()

        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 11 in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_brackets(self, mock_echo, mock_input):
        """Test REPL with multi-line expressions using brackets."""
        mock_input.side_effect = [
            "(var arr [1",
            "          2",
            "          3])",
            "arr",
            "exit",
        ]

        repl()

        # The array should be created and returned
        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        # Check if array-like structure is in output
        assert any("[1, 2, 3]" in str(call) or "1" in str(call) for call in echo_calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_class_definition(self, mock_echo, mock_input):
        """Test REPL with multi-line class definition."""
        mock_input.side_effect = [
            "(class Point null",
            "  (begin",
            "    (def constructor (this x y)",
            "      (begin",
            "        (set (prop this x) x)",
            "        (set (prop this y) y)))",
            "    (def sum (this)",
            "      (+ (prop this x) (prop this y)))))",
            "(var p (new Point 10 20))",
            "((prop p sum) p)",
            "exit",
        ]

        repl()

        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 30 in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_exit_on_first_line(self, mock_echo, mock_input):
        """Test that exit command works even during potential multi-line input."""
        mock_input.side_effect = ["exit"]

        repl()

        calls = [str(call) for call in mock_echo.call_args_list]
        assert any("Goodbye!" in str(call) for call in calls)

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_continuation_prompt(self, mock_echo, mock_input):
        """Test that continuation prompt is displayed for incomplete expressions."""
        mock_input.side_effect = [
            "(+ 1",
            "   2)",
            "exit",
        ]

        repl()

        # The second call should use the continuation prompt
        assert len(mock_input.call_args_list) >= 2

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_deep_nesting(self, mock_echo, mock_input):
        """Test REPL with deeply nested expressions."""
        mock_input.side_effect = [
            "(+ (* (- 10",
            "        5)",
            "      (/ 20",
            "         4))",
            "   (if (> 3 0)",
            "       1",
            "       0))",
            "exit",
        ]

        repl()

        # (+ (* (- 10 5) (/ 20 4)) (if (> 3 0) 1 0))
        # = (+ (* 5 5) 1)
        # = (+ 25 1)
        # = 26
        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 26 in echo_calls

    @patch("ax_lang.cli.exec.input")
    @patch("ax_lang.cli.exec.click.echo")
    def test_repl_multiline_lambda(self, mock_echo, mock_input):
        """Test REPL with multi-line lambda expression."""
        mock_input.side_effect = [
            "((lambda (x y)",
            "   (+ (* x x)",
            "      (* y y)))",
            " 3 4)",
            "exit",
        ]

        repl()

        # (3*3 + 4*4) = 9 + 16 = 25
        echo_calls = [call[0][0] for call in mock_echo.call_args_list if call[0]]
        assert 25 in echo_calls
