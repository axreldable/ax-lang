# command history support for Unix/Mac
import logging
import readline

import click
from ax_lang.interpreter.ax_lang import AxLang
from ax_lang.interpreter.environment import GlobalEnvironment
from ax_lang.parser.parser import get_ast


def eval_global(src, eva):
    expr = get_ast(f"(begin {src})")
    return eva.eval(expr)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """AxLang interpreter command line interface.

    Run without arguments to start the interactive REPL.
    """
    if ctx.invoked_subcommand is None:
        # No subcommand provided, start REPL
        repl()


@cli.command()
@click.argument("expression")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def expr(expression, debug):
    """Execute an AxLang expression directly.

    Examples:
        axlang expr "((lambda (x) (* x x)) 2)"
        axlang expr "((lambda (x) (* x x)) 2)" --debug
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    eva = AxLang()
    result = eval_global(expression, eva)
    click.echo(result)


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
def file(filepath):
    """Execute an AxLang file.

    Example: axlang file examples/test.ax
    """
    eva = AxLang()
    with open(filepath) as file:
        file_src = file.read()
    result = eval_global(file_src, eva)
    click.echo(result)


def repl():
    """Start the AxLang interactive REPL."""
    eva = AxLang()

    click.echo("AxLang Interactive Interpreter")
    click.echo(f"Version: {GlobalEnvironment.lookup('VERSION')}")
    click.echo('Type "exit" or "quit" to leave the REPL')
    if readline:
        click.echo("Command history enabled (use Up/Down arrows)\n")

    while True:
        try:
            # Read input using built-in input() which works with readline
            user_input = input("axlang> ")

            # Check for exit commands
            if user_input.strip().lower() in ("exit", "quit", "q"):
                click.echo("Goodbye!")
                break

            # Skip empty input
            if not user_input.strip():
                continue

            # Evaluate and print result
            # Parse the expression without wrapping in begin to maintain state
            expr = get_ast(user_input)
            result = eva.eval(expr)
            click.echo(result)

        except EOFError:
            # Handle Ctrl+D
            click.echo("\nGoodbye!")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C
            click.echo("\nUse 'exit' or 'quit' to leave the REPL")
            continue
        except Exception as error:
            # Handle evaluation errors
            click.echo(f"Error: {error}", err=True)


if __name__ == "__main__":
    cli()
