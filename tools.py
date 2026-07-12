def calculator(expression: str):

    """
    Evaluate a mathematical expression.

    """

    try:

        result = eval(expression)

        return result

    except Exception:

        return None