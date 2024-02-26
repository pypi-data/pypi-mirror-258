"""Console script for toyapp."""

import sys

import click

from toyapp.toyapp import math_func


@click.command()
@click.option("--quiet", "-q", is_flag=True, help="Don't print the result")
@click.argument("num1", type=click.FLOAT)
@click.argument("num2", type=click.FLOAT)
@click.argument("operation", default="+", type=click.STRING)
def main(quiet: bool, num1: float, num2: float, operation: str):
    """Perform simple arithmetic operations given two numbers and an operator.

    If operator is ommited, the default is addition.
    To prevent * being interpreted as a wildcard, use quotes around
    the operator.

    --quiet, -q: Don't print the leading message, just return the result.
    num1: float - The first number
    num2: float - The second number
    operation: str - The operation to perform on the two numbers

    Evaluates the expression num1 operation num2 and prints the result.
    """
    answer = math_func(num1, num2, operation)
    if not quiet:
        print(f"\n\tThe answer to {num1} {operation} {num2} = {answer:.2f}\n")
        return 0
    print(f"{answer:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
