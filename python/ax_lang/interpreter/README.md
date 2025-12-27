# ax-lang Interpreter

A tree-walking interpreter for the ax-lang programming language. This interpreter evaluates Abstract Syntax Trees (AST) produced by the parser and executes ax-lang programs.

## Overview

The interpreter implements a complete execution environment for ax-lang, featuring:

- **Environment-based variable scoping** with lexical scope
- **First-class functions** with closures
- **Object-oriented programming** with classes and inheritance
- **Module system** for code organization
- **Syntactic sugar transformations** for developer convenience
- **Built-in native functions** for common operations

## Architecture

The interpreter consists of three main components:

### 1. AxLang (ax_lang.py)

The main interpreter class that evaluates AST nodes using a tree-walking approach.

### 2. Environment (environment.py)

Manages variable scopes and bindings using a hierarchical environment chain.

### 3. Transformer (transformer.py)

Performs Just-In-Time (JIT) transformations of syntactic sugar into core language constructs.

## Quick Start

```python
from ax_lang.interpreter.ax_lang import AxLang

# Create interpreter instance
ax = AxLang()

# Evaluate expressions
result = ax.eval(42)                           # 42
result = ax.eval('"hello"')                    # "hello"
result = ax.eval(["+", 2, 3])                  # 5
result = ax.eval(["var", "x", 10])             # 10
result = ax.eval("x")                          # 10
```

## Core Features

### Self-Evaluating Expressions

Numbers and strings evaluate to themselves:

```python
ax.eval(42)          # 42
ax.eval('"hello"')   # "hello"
```

### Variables

**Declaration:**
```python
ax.eval(["var", "x", 10])              # Declare x = 10
ax.eval(["var", "name", '"Alice"'])    # Declare name = "Alice"
```

**Access:**
```python
ax.eval("x")                           # Access variable x
```

**Assignment:**
```python
ax.eval(["set", "x", 20])              # Update x to 20
```

**Built-in Variables:**
- `null` → `None`
- `true` → `True`
- `false` → `False`

### Blocks

Sequential expressions with local scope:

```python
ax.eval([
    "begin",
    ["var", "x", 10],
    ["var", "y", 20],
    ["+", "x", "y"]
])  # 30
```

### Control Flow

**If Expression:**
```python
ax.eval([
    "if",
    [">", "x", 10],
    "Greater",
    "Less or equal"
])
```

**While Loop:**
```python
ax.eval([
    "while",
    ["<", "counter", 10],
    ["++", "counter"]
])
```

**Switch Expression** (syntactic sugar):
```python
ax.eval([
    "switch",
    [["==", "x", 10], 100],
    [[">", "x", 10], 200],
    ["else", 300]
])
```

**For Loop** (syntactic sugar):
```python
ax.eval([
    "for",
    ["var", "i", 0],          # init
    ["<", "i", 10],           # condition
    ["set", "i", ["+", "i", 1]],  # modifier
    ["print", "i"]            # body
])
```

### Functions

**Lambda Functions:**
```python
ax.eval([
    "lambda",
    ["x", "y"],              # parameters
    ["+", "x", "y"]          # body
])  # Returns function object
```

**Function Definition** (syntactic sugar for lambda):
```python
ax.eval([
    "def",
    "square",                # name
    ["x"],                   # parameters
    ["*", "x", "x"]          # body
])

ax.eval(["square", 5])       # 25
```

**Closures:**
```python
ax.eval([
    "begin",
    ["var", "counter", 0],
    ["def", "increment", [],
        ["set", "counter", ["+", "counter", 1]]
    ],
    ["increment"],           # counter = 1
    ["increment"]            # counter = 2
])
```

**Recursive Functions:**
```python
ax.eval([
    "def", "factorial", ["n"],
    ["if", ["==", "n", 1],
        1,
        ["*", "n", ["factorial", ["-", "n", 1]]]
    ]
])

ax.eval(["factorial", 5])    # 120
```

### Classes and OOP

**Class Declaration:**
```python
ax.eval([
    "class", "Point", "null",    # name, parent
    ["begin",
        ["def", "constructor", ["this", "x", "y"],
            ["begin",
                ["set", ["prop", "this", "x"], "x"],
                ["set", ["prop", "this", "y"], "y"]
            ]
        ],
        ["def", "calc", ["this"],
            ["+", ["prop", "this", "x"], ["prop", "this", "y"]]
        ]
    ]
])
```

**Instantiation:**
```python
ax.eval(["var", "p", ["new", "Point", 10, 20]])
```

**Property Access:**
```python
ax.eval(["prop", "p", "x"])                    # 10
```

**Method Invocation:**
```python
ax.eval([["prop", "p", "calc"], "p"])          # 30
```

**Inheritance:**
```python
ax.eval([
    "class", "Point3D", "Point",    # Point3D extends Point
    ["begin",
        ["def", "constructor", ["this", "x", "y", "z"],
            ["begin",
                # Call parent constructor
                [["prop", ["super", "Point3D"], "constructor"], "this", "x", "y"],
                ["set", ["prop", "this", "z"], "z"]
            ]
        ],
        ["def", "calc", ["this"],
            ["+",
                # Call parent method
                [["prop", ["super", "Point3D"], "calc"], "this"],
                ["prop", "this", "z"]
            ]
        ]
    ]
])
```

### Modules

**Module Declaration:**
```python
ax.eval([
    "module", "math",
    ["begin",
        ["def", "square", ["x"], ["*", "x", "x"]],
        ["var", "PI", 3.14]
    ]
])
```

**Module Import:**
```python
# Imports from python/ax_lang/interpreter/modules/math.ax
ax.eval(["import", "math"])

# Access module members
ax.eval([["prop", "math", "square"], 5])       # 25
ax.eval(["prop", "math", "MAX_VALUE"])         # 1000
```

### Syntactic Sugar

The interpreter automatically transforms syntactic sugar into core constructs:

**Increment/Decrement:**
```python
ax.eval(["++", "x"])    # Transformed to: ["set", "x", ["+", "x", 1]]
ax.eval(["--", "y"])    # Transformed to: ["set", "y", ["-", "y", 1]]
```

**Compound Assignment:**
```python
ax.eval(["+=", "count", 5])    # ["set", "count", ["+", "count", 5]]
ax.eval(["-=", "total", 10])   # ["set", "total", ["-", "total", 10]]
```

## Built-in Functions

The global environment provides these native functions:

### Arithmetic
- `+` - Addition
- `-` - Subtraction (unary negation if one argument)
- `*` - Multiplication
- `/` - Division

### Comparison
- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal
- `==` - Equality

### I/O
- `print` - Print values to stdout

## Environment Chain

The interpreter maintains a chain of environments for variable resolution:

```
Global Environment
    └─> Module/Class Environment
            └─> Function Activation Environment
                    └─> Block Environment
```

Each environment can:
- **define(name, value)** - Create a new binding
- **assign(name, value)** - Update an existing binding
- **lookup(name)** - Retrieve a value
- **resolve(name)** - Find the environment containing a binding

## API Reference

### AxLang Class

```python
class AxLang:
    def __init__(self)
        """Creates an ax-lang instance with global environment"""

    def eval(self, expr: Number | str | list, env: Environment = None)
        """Evaluates an expression in the given environment

        Args:
            expr: AST node (number, string, or list)
            env: Environment for evaluation (defaults to global)

        Returns:
            Result of evaluation
        """
```

### Environment Class

```python
class Environment:
    def __init__(self, record: dict, parent: Environment = None)
        """Create environment with local bindings and parent scope"""

    def define(self, name, value)
        """Creates a variable with given name and value"""

    def assign(self, name, value)
        """Updates an existing variable"""

    def lookup(self, name)
        """Returns the value of a variable"""

    def resolve(self, name) -> Environment
        """Returns the environment where variable is defined"""
```

### Transformer Class

```python
class Transformer:
    def def_to_lambda(self, def_expr: list) -> list
        """Transforms function definition to lambda"""

    def switch_to_if(self, switch_expr: list) -> list
        """Transforms switch to nested if expressions"""

    def for_to_while(self, for_expr: list) -> list
        """Transforms for-loop to while-loop"""

    def inc_to_set(self, expr: list) -> list
        """Transforms ++ to set expression"""

    def dec_to_set(self, expr: list) -> list
        """Transforms -- to set expression"""

    def plus_assign_to_set(self, expr: list) -> list
        """Transforms += to set expression"""

    def minus_assign_to_set(self, expr: list) -> list
        """Transforms -= to set expression"""
```

## Testing

Run the interpreter test suite:

```bash
pytest python/tests/interpreter/
```

Test categories:
- `test_eval.py` - Basic evaluation
- `test_variable.py` - Variable operations
- `test_math.py` - Arithmetic operations
- `test_control_flow.py` - Conditionals and loops
- `test_blocks.py` - Block scoping
- `test_syntactic_sugar.py` - Syntactic sugar transformations
- `functions/` - Lambda, user-defined, and recursive functions
- `oop/` - Classes and inheritance
- `modules/` - Module system

## Implementation Notes

1. **Tree-Walking Interpreter**: Directly interprets AST nodes without compilation
2. **Lexical Scoping**: Variables are resolved using static scope chains
3. **First-Class Functions**: Functions are values that can be passed and returned
4. **JIT Transformation**: Syntactic sugar is transformed during evaluation
5. **Environment as Objects**: Classes and modules are implemented as environments
6. **Property Access**: Uses special `prop` expressions for object properties

## Files

- `ax_lang.py` - Main interpreter implementation
- `environment.py` - Environment and scope management
- `transformer.py` - Syntactic sugar transformations
- `modules/` - Standard library modules (e.g., math.ax)

## Example: Complete Program

```python
from ax_lang.interpreter.ax_lang import AxLang

ax = AxLang()

# Define and use a factorial function
ax.eval([
    "begin",
    ["def", "factorial", ["n"],
        ["if", ["==", "n", 1],
            1,
            ["*", "n", ["factorial", ["-", "n", 1]]]
        ]
    ],
    ["factorial", 5]  # 120
])
```