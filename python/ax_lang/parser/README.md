# ax-lang Parser

A Python-based S-expression parser for the ax-lang programming language. This parser converts ax-lang source code into Abstract Syntax Trees (AST) for further processing by the interpreter.

## Overview

The parser is built using [syntax-cli](https://github.com/DmitrySoshnikov/syntax), a tool for generating parsers from BNF grammars. It transforms ax-lang's Lisp-like syntax into JSON-compatible Python data structures.

## Prerequisites

Install syntax-cli globally:

```bash
npm install -g syntax-cli
```

## Grammar

The parser is defined by the BNF grammar in `ax-lang-grammar.bnf.g`, which specifies:

### Lexical Tokens
- **NUMBER**: Integer literals (e.g., `42`, `100`)
- **STRING**: String literals (e.g., `"Hello World"`)
- **SYMBOL**: Identifiers and operators (e.g., `foo`, `+`, `*`, `==`)

### Syntax Rules
- **Atom**: Numbers, strings, or symbols
- **List**: S-expressions in the form `(operator operand1 operand2 ...)`
- **Exp**: An expression, which can be either an atom or a list

## API

### `get_ast(expr: str) -> Number | str | list`

Parses an ax-lang expression and returns its AST representation.

**Parameters:**
- `expr` (str): The ax-lang source code to parse

**Returns:**
- Number, string, or list representing the AST

**Example:**

```python
from ax_lang.parser.parser import get_ast

# Parse a simple arithmetic expression
ast = get_ast("(+ 1 2)")
# Returns: ["+", 1, 2]

# Parse a function definition
ast = get_ast("(def square (x) (* x x))")
# Returns: ["def", "square", ["x"], ["*", "x", "x"]]

# Parse an atom
ast = get_ast("42")
# Returns: 42
```

## Examples

### Atoms
```python
get_ast("42")           # 42
get_ast('"Hello"')      # "Hello"
get_ast("foo")          # "foo"
```

### Lists
```python
get_ast("(+ 5 x)")                    # ["+", 5, "x"]
get_ast("(print \"hello\")")          # ["print", "hello"]
```

### Nested Expressions
```python
get_ast("(+ (+ 3 2) 5)")              # ["+", ["+", 3, 2], 5]
```

### Lambda Functions
```python
get_ast("((lambda (x) (* x x)) 2)")
# Returns: [["lambda", ["x"], ["*", "x", "x"]], 2]
```

### Function Definitions
```python
get_ast("""
(def factorial (x)
    (if (== x 1)
        1
        (* x (factorial (- x 1)))))
""")
# Returns: ["def", "factorial", ["x"],
#           ["if", ["==", "x", 1], 1, ["*", "x", ["factorial", ["-", "x", 1]]]]]
```

### Classes
```python
get_ast("""
(class Point null
    (begin
        (def constructor (this x y)
            (begin
                (set (prop this x) x)
                (set (prop this y) y)))

        (def calc (this)
            (+ (prop this x) (prop this y)))
    ))
""")
# Returns AST representation of class definition
```

## Testing

Run the test suite:

```bash
make test
```

Or use pytest:

```bash
pytest tests/parser/test_parser.py
```

## Implementation Details

The parser works by:

1. Invoking `syntax-cli` as a subprocess with the grammar file and input expression
2. Capturing the output from syntax-cli
3. Extracting the "Parsed value" section from the output
4. Removing ANSI color codes
5. Parsing the JSON representation into Python data structures

## Development

To modify the grammar:

1. Edit `ax-lang-grammar.bnf.g`
2. Test your changes using the Makefile:
   ```bash
   make test
   ```
3. The parser will automatically use the updated grammar on the next invocation

## Files

- `ax-lang-grammar.bnf.g` - BNF grammar definition
- `parser.py` - Main parser implementation
- `Makefile` - Test commands for grammar validation

## Notes

- The parser uses LALR1 parsing mode for efficient parsing
- All whitespace is automatically skipped during tokenization
- String literals can contain any characters except double quotes
- Symbols support alphanumeric characters plus: `-`, `+`, `*`, `=`, `<`, `>`, `/`