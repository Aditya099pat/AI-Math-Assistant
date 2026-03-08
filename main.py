from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from sympy import (
    symbols,
    sympify,
    diff,
    integrate,
    solve,
    expand,
    factor,
    simplify,
    limit,
    Matrix,
    sin,
    cos,
    tan,
    asin,
    acos,
    atan,
    pi,
    N,
)
from sympy.core.sympify import SympifyError

load_dotenv()


@tool
def calculator(a: float, b: float, operation: str) -> str:
    """Perform basic arithmetic operations.
    operation must be one of: add, subtract, multiply, divide, power
    """
    operation = operation.lower().strip()

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero is not allowed."
        result = a / b
    elif operation == "power":
        result = a ** b
    else:
        return "Error: Invalid operation. Use add, subtract, multiply, divide, or power."

    print("Calculator tool has been called.")
    return f"Result: {result}"


@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user."""
    print("Hello tool has been called.")
    return f"Hello {name}, I hope you are well today."


@tool
def simplify_expression(expression: str) -> str:
    """Simplify an algebraic expression. Example: '(x**2 + 2*x + 1)/(x+1)' """
    try:
        expr = sympify(expression)
        result = simplify(expr)
        print("Simplify tool has been called.")
        return f"Simplified expression: {result}"
    except SympifyError:
        return "Error: Invalid algebraic expression."


@tool
def expand_expression(expression: str) -> str:
    """Expand an algebraic expression. Example: '(x+1)*(x+2)' """
    try:
        expr = sympify(expression)
        result = expand(expr)
        print("Expand tool has been called.")
        return f"Expanded expression: {result}"
    except SympifyError:
        return "Error: Invalid algebraic expression."


@tool
def factor_expression(expression: str) -> str:
    """Factor an algebraic expression. Example: 'x**2 + 3*x + 2' """
    try:
        expr = sympify(expression)
        result = factor(expr)
        print("Factor tool has been called.")
        return f"Factored expression: {result}"
    except SympifyError:
        return "Error: Invalid algebraic expression."


@tool
def derivative(expression: str, variable: str) -> str:
    """Find the derivative of an expression with respect to a variable.
    Example: expression='x**3 + 2*x', variable='x'
    """
    try:
        var = symbols(variable)
        expr = sympify(expression)
        result = diff(expr, var)
        print("Derivative tool has been called.")
        return f"Derivative of {expression} with respect to {variable}: {result}"
    except SympifyError:
        return "Error: Invalid expression or variable."


@tool
def integral(expression: str, variable: str) -> str:
    """Find the indefinite integral of an expression with respect to a variable.
    Example: expression='x**2', variable='x'
    """
    try:
        var = symbols(variable)
        expr = sympify(expression)
        result = integrate(expr, var)
        print("Integral tool has been called.")
        return f"Indefinite integral of {expression} with respect to {variable}: {result} + C"
    except SympifyError:
        return "Error: Invalid expression or variable."


@tool
def definite_integral(expression: str, variable: str, lower: float, upper: float) -> str:
    """Find the definite integral of an expression over given bounds.
    Example: expression='x**2', variable='x', lower=0, upper=2
    """
    try:
        var = symbols(variable)
        expr = sympify(expression)
        result = integrate(expr, (var, lower, upper))
        print("Definite integral tool has been called.")
        return f"Definite integral of {expression} from {lower} to {upper} with respect to {variable}: {result}"
    except SympifyError:
        return "Error: Invalid expression or variable."


@tool
def compute_limit(expression: str, variable: str, point: str, direction: str = "+") -> str:
    """Compute the limit of an expression.
    direction can be '+', '-', or '+-'
    Example: expression='sin(x)/x', variable='x', point='0'
    """
    try:
        var = symbols(variable)
        expr = sympify(expression)
        point_expr = sympify(point)

        dir_value = direction.strip()
        if dir_value not in ["+", "-", "+-"]:
            return "Error: direction must be '+', '-', or '+-'."

        result = limit(expr, var, point_expr, dir=dir_value)
        print("Limit tool has been called.")
        return f"Limit of {expression} as {variable} approaches {point} from direction '{dir_value}': {result}"
    except Exception as e:
        return f"Error: Could not compute limit. {str(e)}"


@tool
def solve_equation(equation: str, variable: str) -> str:
    """Solve an algebraic equation for a variable.
    Supports both:
    'x**2 - 5*x + 6'
    'x**2 - 5*x + 6 = 0'
    """
    try:
        var = symbols(variable)

        if "=" in equation:
            left, right = equation.split("=", 1)
            expr = sympify(left) - sympify(right)
        else:
            expr = sympify(equation)

        result = solve(expr, var)
        print("Solve equation tool has been called.")
        return f"Solutions for {equation} with respect to {variable}: {result}"
    except SympifyError:
        return "Error: Invalid equation or variable."


@tool
def evaluate_trig_function(function_name: str, value: str, angle_unit: str = "radians") -> str:
    """Evaluate a trigonometric function at a given value."""
    try:
        fn = function_name.lower().strip()
        unit = angle_unit.lower().strip()
        val = sympify(value)

        if unit == "degrees" and fn in ["sin", "cos", "tan"]:
            val = val * pi / 180
        elif unit not in ["radians", "degrees"]:
            return "Error: angle_unit must be 'radians' or 'degrees'."

        trig_map = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "asin": asin,
            "acos": acos,
            "atan": atan,
        }

        if fn not in trig_map:
            return "Error: function_name must be one of sin, cos, tan, asin, acos, atan."

        result = trig_map[fn](val)
        numeric_result = N(result)

        print("Trigonometry tool has been called.")
        return f"{fn}({value}) in {angle_unit}: exact = {result}, approximate = {numeric_result}"
    except Exception as e:
        return f"Error: Could not evaluate trigonometric function. {str(e)}"


@tool
def trig_simplify(expression: str) -> str:
    """Simplify a trigonometric expression."""
    try:
        expr = sympify(expression)
        result = simplify(expr)
        print("Trig simplify tool has been called.")
        return f"Trig simplified expression: {result}"
    except Exception as e:
        return f"Error: Could not simplify trigonometric expression. {str(e)}"


@tool
def create_matrix(matrix_data: str) -> str:
    """Create a matrix from a string representation."""
    try:
        matrix_list = sympify(matrix_data)
        mat = Matrix(matrix_list)
        print("Create matrix tool has been called.")
        return f"Matrix:\n{mat}"
    except Exception as e:
        return f"Error: Could not create matrix. {str(e)}"


@tool
def matrix_determinant(matrix_data: str) -> str:
    """Compute the determinant of a square matrix."""
    try:
        mat = Matrix(sympify(matrix_data))
        if mat.rows != mat.cols:
            return "Error: Determinant is only defined for square matrices."
        result = mat.det()
        print("Matrix determinant tool has been called.")
        return f"Determinant: {result}"
    except Exception as e:
        return f"Error: Could not compute determinant. {str(e)}"


@tool
def matrix_inverse(matrix_data: str) -> str:
    """Compute the inverse of a square matrix."""
    try:
        mat = Matrix(sympify(matrix_data))
        if mat.rows != mat.cols:
            return "Error: Inverse is only defined for square matrices."
        if mat.det() == 0:
            return "Error: Matrix is singular and has no inverse."
        result = mat.inv()
        print("Matrix inverse tool has been called.")
        return f"Inverse matrix:\n{result}"
    except Exception as e:
        return f"Error: Could not compute inverse. {str(e)}"


@tool
def matrix_multiply(matrix_a: str, matrix_b: str) -> str:
    """Multiply two matrices."""
    try:
        mat_a = Matrix(sympify(matrix_a))
        mat_b = Matrix(sympify(matrix_b))

        if mat_a.cols != mat_b.rows:
            return "Error: Number of columns of first matrix must equal number of rows of second matrix."

        result = mat_a * mat_b
        print("Matrix multiplication tool has been called.")
        return f"Matrix product:\n{result}"
    except Exception as e:
        return f"Error: Could not multiply matrices. {str(e)}"


@tool
def matrix_eigenvalues(matrix_data: str) -> str:
    """Compute eigenvalues of a square matrix."""
    try:
        mat = Matrix(sympify(matrix_data))
        if mat.rows != mat.cols:
            return "Error: Eigenvalues are only defined for square matrices."

        result = mat.eigenvals()
        print("Matrix eigenvalues tool has been called.")
        return f"Eigenvalues: {result}"
    except Exception as e:
        return f"Error: Could not compute eigenvalues. {str(e)}"


def main():
    model = ChatOpenAI(
        model="openrouter/auto",
        temperature=0,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:3000",
            "X-OpenRouter-Title": "My First AI Project",
        },
    )

    tools = [
        calculator,
        say_hello,
        simplify_expression,
        expand_expression,
        factor_expression,
        derivative,
        integral,
        definite_integral,
        compute_limit,
        solve_equation,
        evaluate_trig_function,
        trig_simplify,
        create_matrix,
        matrix_determinant,
        matrix_inverse,
        matrix_multiply,
        matrix_eigenvalues,
    ]

    agent = create_agent(model=model, tools=tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations, algebra, calculus, trigonometry, matrices, or chat with me.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            break

        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]}
            )

            print("\nAssistant: ", end="")
            for message in result["messages"]:
                if getattr(message, "type", "") == "ai" and message.content:
                    print(message.content)

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()