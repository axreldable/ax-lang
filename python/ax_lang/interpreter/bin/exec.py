import argparse

from ax_lang.interpreter.ax_lang import AxLang
from ax_lang.interpreter.ax_lang import GlobalEnvironment
from ax_lang.interpreter.parser import get_lisp_representation


def eval_global(src, eva):
    expr = get_lisp_representation(f"(begin {src})")
    return eva.eval(expr)


def main():
    # Create a parser
    parser = argparse.ArgumentParser(description="A simple argparse example.")

    # Add arguments
    parser.add_argument("mode", help="execution mode")
    parser.add_argument("expr", help="eva expression or file path")

    # Parse the arguments
    args = parser.parse_args()
    mode = args.mode
    expr = args.expr

    eva = AxLang(GlobalEnvironment)

    if mode == "e":
        rez = eval_global(expr, eva)
        print(rez)

    if mode == "f":
        file_src = None
        with open(expr) as f:
            file_src = f.read()
        rez = eval_global(file_src, eva)
        print(rez)


# python ax_lang/interpreter/bin/exec.py e "((lambda (x) (* x x)) 2)"
# python ax_lang/interpreter/bin/exec.py f ax_lang/interpreter/test.ax
if __name__ == "__main__":
    main()
