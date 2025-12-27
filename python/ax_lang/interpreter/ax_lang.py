import logging
import re
import types
from numbers import Number

from ax_lang.interpreter.environment import Environment
from ax_lang.interpreter.environment import GlobalEnvironment
from ax_lang.interpreter.transformer import Transformer
from ax_lang.parser.parser import get_ast


logger = logging.getLogger(__name__)


class AxLang:
    def __init__(self):
        """Creates an ax-lang instance with global environment"""
        self.global_env = GlobalEnvironment
        self.transformer = Transformer()

    def _is_variable_name(self, expr):
        return isinstance(expr, str) and bool(
            re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", expr)
        )

    def _is_function_name(self, expr):
        # fmt: off
        native_function_names = {"+", "-", "*", "/", ">", ">=", "<", "<=", "==", "print"}
        # fmt: on
        return isinstance(expr, str) and expr in native_function_names

    def _eval_block(self, block, env):
        logger.debug(f"Evaluating block=`{block}`...")
        rez = None
        for expr in block:
            rez = self.eval(expr, env)
        return rez

    def _eval_body(self, body, env):
        if body[0] == "begin":
            return self._eval_block(body[1:], env)
        logger.debug(f"Evaluating body: `{body}`...")
        return self.eval(body, env)

    def _call_user_defined_function(self, fn, eval_args):
        activation_record = {}
        for i, param in enumerate(fn["params"]):
            activation_record[param] = eval_args[i]
        activation_env = Environment(activation_record, fn["env"])
        return self._eval_body(fn["body"], activation_env)

    def eval(self, expr: Number | str | list, env: Environment = None):
        logger.debug(f"Expr: {expr}")
        env = self.global_env if env is None else env
        # Self-evaluating expressions:
        if isinstance(expr, Number):
            return expr

        if isinstance(expr, str):
            if expr[0] == '"' and expr[-1] == '"':
                return expr[1:-1]

        # Variable declaration:
        if expr[0] == "var":
            _, name, value = expr
            return env.define(name, self.eval(value, env))

        # Variable update:
        if expr[0] == "set":
            _, ref, value = expr

            # Assignment to property
            if ref[0] == "prop":
                _, instance, prop_name = ref
                instance_env = self.eval(instance, env)
                return instance_env.define(prop_name, self.eval(value, env))

            return env.assign(ref, self.eval(value, env))

        # Variable access:
        if self._is_variable_name(expr):
            return env.lookup(expr)

        # Block: sequence of expressions
        if expr[0] == "begin":
            block_env = Environment({}, env)
            return self._eval_block(expr[1:], block_env)

        # if-expression
        if expr[0] == "if":
            _, condition, consequent, alternate = expr
            if self.eval(condition, env):
                return self.eval(consequent, env)
            return self.eval(alternate, env)

        # while-expression
        if expr[0] == "while":
            _, condition, body = expr
            rez = None
            while self.eval(condition, env):
                rez = self.eval(body, env)
            return rez

        # build-in functions
        if self._is_function_name(expr):
            return env.lookup(expr)

        # function declaration
        if expr[0] == "def":
            # JIT-transpile to a variable declaration
            var_expr = self.transformer.def_to_lambda(expr)
            return self.eval(var_expr, env)

        # switch-expression (syntactic sugar for if-expression)
        if expr[0] == "switch":
            if_exp = self.transformer.switch_to_if(expr)
            return self.eval(if_exp, env)

        # for-loop (syntactic sugar for while-loop)
        if expr[0] == "for":
            while_exp = self.transformer.for_to_while(expr)
            return self.eval(while_exp, env)

        # ++ (syntactic sugar for set operation)
        if expr[0] == "++":
            set_exp = self.transformer.inc_to_set(expr)
            return self.eval(set_exp, env)

        # ++ (syntactic sugar for set operation)
        if expr[0] == "--":
            set_exp = self.transformer.dec_to_set(expr)
            return self.eval(set_exp, env)

        # += (syntactic sugar for set operation)
        if expr[0] == "+=":
            set_exp = self.transformer.plus_assign_to_set(expr)
            return self.eval(set_exp, env)

        # -= (syntactic sugar for set operation)
        if expr[0] == "-=":
            set_exp = self.transformer.minus_assign_to_set(expr)
            return self.eval(set_exp, env)

        # lambda declaration
        if expr[0] == "lambda":
            _, params, body = expr
            rez_lambda = {
                "params": params,
                "body": body,
                "env": env,
            }
            logger.debug(f"Evaluated lambda: `{rez_lambda}`...")
            return rez_lambda

        # Class declaration (class name parent body)
        if expr[0] == "class":
            _, name, parent, body = expr
            parent_env = self.eval(parent, env) or env
            class_env = Environment({}, parent_env)
            # body is evaluated in the class environment
            self._eval_body(body, class_env)
            # Class is accessible by name
            return env.define(name, class_env)

        # Super expressions (super <class_name>)
        if expr[0] == "super":
            _, class_name = expr
            return self.eval(class_name, env).parent

        # Class instantiation (new class arguments)
        if expr[0] == "new":
            class_env = self.eval(expr[1], env)
            # An instance of class is an environment
            instance_env = Environment({}, class_env)
            eval_args = [self.eval(arg, env) for arg in expr[2:]]
            self._call_user_defined_function(
                class_env.lookup("constructor"), [instance_env, *eval_args]
            )
            return instance_env

        # property access: (prop <instance> <name>)
        if expr[0] == "prop":
            _, instance, name = expr
            instance_env = self.eval(instance, env)
            return instance_env.lookup(name)

        # module declaration: (module <name> <body>)
        if expr[0] == "module":
            _, name, body = expr
            module_env = Environment({}, env)
            self._eval_body(body, module_env)
            return env.define(name, module_env)

        # module import: (import <name>)
        if expr[0] == "import":
            _, name = expr

            module_src = None
            local_dirs = __file__.split("/")
            local_dirs = local_dirs[: (len(local_dirs) - 1)]
            local_path = "/".join(local_dirs)
            with open(f"{local_path}/modules/{name}.ax") as f:
                module_src = f.read()

            body = get_ast(f"(begin {module_src})")
            module_expr = ["module", name, body]
            return self.eval(module_expr, env)

        # Function calls:
        if isinstance(expr, list):
            fn = self.eval(expr[0], env)
            logger.debug(f"Processing fn: `{fn}`...")
            eval_args = [self.eval(arg, env) for arg in expr[1:]]

            # 1. Native functions
            if isinstance(fn, types.FunctionType):
                logger.debug(f"Applying fn: `{fn.__name__}` to args: `{eval_args}`...")
                return fn(*eval_args)

            # 2. User-defined functions
            # it's type dict here
            if isinstance(fn, dict):
                logger.debug(f"Processing User-defined function `{fn}`...")
                return self._call_user_defined_function(fn, eval_args)

            raise NotImplementedError(fn)
        raise NotImplementedError(expr)
