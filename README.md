# Axreldable programming language

[![PyPI version](https://img.shields.io/pypi/v/ax-lang?label=PyPI)](https://pypi.org/project/ax-lang/)
[![codecov](https://codecov.io/gh/axreldable/ax-lang/branch/master/graph/badge.svg)](https://codecov.io/gh/axreldable/ax-lang)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://axreldable.github.io/ax-lang/)

## Installation

### 1. Install the latest version from PyPI

```bash
pip install ax-lang
```

## Specification

[Language specification](https://axreldable.github.io/ax-lang/latest/specification/) can be found in the documentation.


## Examples

Find AxLang [example](examples/ax-lang) and their [python](examples/python) equivalents.

## Usage

After installation, you can use the `axlang` command in three different modes:

### Interactive REPL

Start an interactive session to evaluate AxLang expressions:

```bash
axlang
```

Example session:
```
axlang> (+ 2 3)
5
axlang> (var x 10)
10
axlang> (* x x)
100
axlang> exit
Goodbye!
```

### Execute Expression

Evaluate a single AxLang expression directly from the command line:

```bash
axlang expr "((lambda (x) (* x x)) 2)"
```

### Execute File

Run an AxLang program from a file:

```bash
axlang file examples/ax-lang/test.ax
```

---

Built with the help of the great Dmitry Soshnikov's [courses](https://www.udemy.com/user/dmitry-soshnikov/) on
Programming Languages.
