import ast
import operator


# Map safe mathematical operators to Python functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate_node(node):
    """
    Recursively evaluate a safe arithmetic expression.
    """

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("This operator is not supported.")

        left_value = _evaluate_node(node.left)
        right_value = _evaluate_node(node.right)

        return OPERATORS[operator_type](
            left_value,
            right_value
        )

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("This operator is not supported.")

        operand_value = _evaluate_node(node.operand)

        return OPERATORS[operator_type](operand_value)

    raise ValueError("Invalid mathematical expression.")


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    """

    expression = expression.strip()

    if not expression:
        return "No mathematical expression was provided."

    try:
        parsed_expression = ast.parse(
            expression,
            mode="eval"
        )

        result = _evaluate_node(parsed_expression.body)

        return str(result)

    except ZeroDivisionError:
        return "Division by zero is not allowed."

    except (SyntaxError, ValueError, TypeError) as error:
        return f"Invalid calculation: {error}"