def is_expression_complete(expr: str) -> bool:
    """Check if an expression is syntactically complete by counting balanced parentheses.

    Returns True if all parentheses are balanced, False otherwise.
    """
    paren_count = 0
    bracket_count = 0
    in_string = False
    escape_next = False

    for char in expr:
        if escape_next:
            escape_next = False
            continue

        if char == "\\" and in_string:
            escape_next = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "(":
            paren_count += 1
        elif char == ")":
            paren_count -= 1

    # Expression is complete if all brackets are balanced and not in a string
    return paren_count == 0 and bracket_count == 0 and not in_string
