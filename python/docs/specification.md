# AxLang Language Specification

This document provides a specification of the AxLang programming language syntax and semantics.

## Table of Contents

1. [Expression Evaluation](#1-expression-evaluation)
2. [Self-Evaluating Expressions](#2-self-evaluating-expressions)
   - [Numbers](#21-numbers)
   - [Strings](#22-strings)
3. [Binary Operations](#3-binary-operations)
4. [Variable Declaration](#4-variable-declaration)
5. [Assignment Expressions](#5-assignment-expressions)
6. [Variable Access](#6-variable-access)
7. [Block Expressions](#7-block-expressions)
8. [Branching](#8-branching)
   - [If Expressions](#81-if-expressions)
   - [Switch Expressions](#82-switch-expressions)
9. [Loops](#9-loops)
   - [While Loops](#91-while-loops)
   - [For Loops](#92-for-loops)
10. [Functions](#10-functions)
    - [Lambda Expressions](#101-lambda-expressions)
    - [Function Declarations](#102-function-declarations)
    - [Function Calls](#103-function-calls)
11. [Classes](#11-classes)
12. [Modules](#12-modules)

---

## 1. Expression Evaluation

AxLang is based on the paradigm, where programs are composed of [s-expressions](https://en.wikipedia.org/wiki/S-expression) that evaluate to values.

### S-Expressions

AxLang uses **S-expressions** (Symbolic expressions) as its fundamental syntax, the same notation used in Lisp family programming languages. An S-expression is either:

1. An **atom** - a primitive value like a number, string, or symbol
2. A **list** - zero or more S-expressions enclosed in parentheses

**Syntax:**
```
<s-expression> ::= <atom> | (<s-expression>*)
```

**Examples:**

Atoms:
```lisp
42          ; number
"hello"     ; string
foo         ; symbol
```

Lists (prefix notation):
```lisp
(+ 1 2)                    ; function call
(var x 10)                 ; variable declaration
(if (> x 0) "positive" "non-positive")  ; nested expressions
```

**Key Properties:**

- **Prefix notation**: The operator or function name comes first, followed by arguments
  - Instead of `1 + 2`, we write `(+ 1 2)`
  - Instead of `x > 0`, we write `(> x 0)`

- **Uniform structure**: Code and data share the same representation
  - Functions, operators, and special forms all use the same syntax
  - This enables powerful metaprogramming capabilities

- **Explicit grouping**: Parentheses eliminate ambiguity about evaluation order
  - `(+ (* 2 3) 4)` is unambiguous (multiply first, then add)
  - No need for operator precedence rules

**Evaluation:**

S-expressions are evaluated recursively:
1. **Atoms** evaluate to themselves (numbers, strings) or their bound values (symbols)
2. **Lists** are evaluated as function calls or special forms:
   - First element determines the operation
   - Remaining elements are the arguments
   - Arguments are evaluated before being passed (except in special forms like `if`, `var`, etc.)

---

## 2. Self-Evaluating Expressions

Self-evaluating expressions are literals that evaluate to themselves.

### 2.1. Numbers

**Expression:**
```
^[-+]?\d+(\.\d+)?$
```

**Examples:**
```lisp
100
-5.7
```

Numbers are self-evaluating. When the interpreter encounters a numeric literal, it directly returns the number value.

### 2.2. Strings

**Expression:**
```
"<chars>"
```

**Examples:**
```lisp
"hello"
"world"
```

String literals enclosed in double quotes are self-evaluating.

---

## 3. Binary Operations

AxLang supports three categories of binary operations:

**Math Operations:**
```lisp
(+ 5 10)
(* x 15)
(- (/ foo 5) 42)
```

**Comparison Operations:**
```lisp
(< 5 10)
(>= x 15)
(!= foo 42)
```

**Logical Operations:**
```lisp
(or foo default)
(and x y)
(not isValid)
```

All binary operations use prefix notation, where the operator comes first, followed by the operands.

---

## 4. Variable Declaration

**Expression:**
```lisp
(var <name> <value>)
```

**Examples:**
```lisp
(var foo 42)
(var bar (* foo 10))
```

The `var` keyword declares a new variable in the current environment. The variable name is bound to the evaluated value. Variables can be initialized with any expression, including computed values.

---

## 5. Assignment Expressions

**Expression:**
```lisp
(set <name> <value>)
```

**Examples:**
```lisp
(set foo 42)
(set bar (* foo 10))
```

The `set` keyword updates the value of an existing variable. Unlike `var`, `set` does not create new variables - it modifies variables that already exist in the current or parent scopes.

---

## 6. Variable Access

**Expression:**
```
<name>
```

**Examples:**
```lisp
foo
(square 2)
```

Variables are accessed by their name. The interpreter performs identifier resolution by looking up the variable in the current environment. If not found in the current scope, it searches parent scopes recursively.

---

## 7. Block Expressions

**Expression:**
```lisp
(begin <sequence>)
```

**Example:**
```lisp
(begin
  (var foo 42)
  (set bar (* foo 10))
  (+ foo bar))
```

Block expressions group multiple expressions together using the `begin` keyword. Each expression in the block is evaluated sequentially in a new nested environment. The block returns the value of the last expression. Variables declared within a block are scoped to that block.

---

## 8. Branching

### 8.1. If Expressions

**Expression:**
```lisp
(if <condition>
    <consequent>
    <alternate>)
```

**Example:**
```lisp
(if (> x 0)
    (set y 10)
    (begin
      (set y 20)
      (print "exit")))
```

The `if` expression evaluates the condition. If the condition is truthy, the consequent expression is evaluated and returned. Otherwise, the alternate expression is evaluated and returned. Both branches can be any expression, including blocks.

### 8.2. Switch Expressions

**Expression:**
```lisp
(switch (<cond1> <block1>)
        ...
        (<condN> <blockN>)
        (else <alternate>))
```

**Example:**
```lisp
(switch ((> x 1) 100)
        ((= x 1) 200)
        (else 0))
```

**Transformation:**

The `switch` expression is syntactic sugar that transforms into nested `if` expressions:

```lisp
(if <cond1>
    <block1>
    ...
    (if <condN>
        <blockN>
        <alternate>))
```

Switch provides a cleaner syntax for multi-way branching compared to nested if expressions.

---

## 9. Loops

### 9.1. While Loops

**Expression:**
```lisp
(while <condition>
       <block>)
```

**Example:**
```lisp
(while (> x 10)
  (begin
    (-- x)
    (print x)))
```

While loops repeatedly evaluate the body block as long as the condition remains truthy. The loop returns the value of the last iteration of the body.

### 9.2. For Loops

**Expression:**
```lisp
(for <init>
     <condition>
     <modifier>
     <exp>)
```

**Example:**
```lisp
(for (var x 10)
     (> x 0)
     (-- x)
     (print x))
```

**Transformation:**

The `for` loop is syntactic sugar that transforms into:

```lisp
(begin
  <init>
  (while <condition>
    (begin
      <exp>
      <modifier>)))
```

For loops provide a convenient way to express iteration with initialization, condition checking, and modification in a single construct.

---

## 10. Functions

### 10.1. Lambda Expressions

**Expression:**
```lisp
(lambda <args>
        <body>)
```

**Example:**
```lisp
(lambda (x) (* x x))
```

Lambda expressions create anonymous functions with lexical closures. Lambdas are first-class values that can be assigned to variables, passed as arguments, and returned from functions.

### 10.2. Function Declarations

**Expression:**
```lisp
(def <name> <args>
     <body>)
```

**Example:**
```lisp
(def square (x)
  (* x x))
```

**Transformation:**

Function declarations are syntactic sugar that transforms into a variable declaration with a lambda:

```lisp
(var <name>
  (lambda <args>
          <body>))
```

This transformation shows that named functions are simply variables bound to lambda expressions.

### 10.3. Function Calls

**Expression:**
```lisp
(<fn> <args>)
```

**Examples:**
```lisp
(square 2)
((lambda (x) (* x x)) 2)
```

Function calls evaluate the function expression and all argument expressions, then apply the function to the arguments. AxLang supports both built-in native functions and user-defined functions.

---

## 11. Classes

**Expression (class definition):**
```lisp
(class <name> <parent>
       <body>)
```

**Expression (instantiation):**
```lisp
(new <class> <args>)
```

**Example:**
```lisp
(class Point null
  (begin
    (def constructor (self x y)
      ((prop self setX) x)
      ((prop self setY) y))

    (def getX (self)
      (prop self x))

    (def setX (self x)
      (set (prop self x) x))

    (var p (new Point 10 20))
    ((prop p getX))
```

Classes provide object-oriented programming capabilities:

- **Inheritance**: Classes can inherit from a parent class (use `null` for no parent)
- **Constructor**: Special `constructor` method initializes instances
- **Methods**: Functions that operate on instance data
- **Properties**: Instance variables accessed via `prop`
- **Instantiation**: `new` keyword creates class instances

---

## 12. Modules

**Expression (module definition):**
```lisp
(module <name>
        <body>)
```

**Expression (import):**
```lisp
(import <name>)
```

**Example:**
```lisp
(module Math
  (begin
    (def square (x)
      (* x x))

    (var MAX_VALUE 100)))

(import Math)
((prop Math square) 2)
```

Modules provide code organization and namespace management:

- **Module definition**: The `module` keyword creates a named namespace
- **Encapsulation**: Variables and functions defined within a module are scoped to that module
- **Import**: The `import` keyword makes a module available in the current scope
- **Access**: Module members are accessed using the `prop` function

Modules help organize code into logical units and prevent naming conflicts.

---

## Additional Resources

- [API Documentation](api.md)
- [Getting Started Guide](index.md)
- [GitHub Repository](https://github.com/axreldable/ax-lang)
