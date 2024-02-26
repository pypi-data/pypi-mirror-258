"""Main module for the toyapp package. Provides math functions."""


def math_func(num1, num2, opperation):
    """Main function."""
    equation = f"{num1} {opperation} {num2}"
    return eval(equation)
