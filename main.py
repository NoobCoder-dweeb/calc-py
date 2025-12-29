# Additionally, this project uses python generics
from typing import TypeVar, Dict, Callable, Union, Any

T = TypeVar("T", bound=float)


def add[T: (int, float)](x: T, y: T) -> T:
    return x + y


def subtract[T: (int, float)](x: T, y: T) -> T:
    return x - y


def multiply[T: (int, float)](x: T, y: T) -> T:
    return x * y


def divide[T: (int, float)](x: T, y: T) -> float | T:
    if y == 0:
        raise ZeroDivisionError("Divisor cannot be 0")
    return float(x) / float(y)


def modulus[T: (int, float)](x: T, y: T) -> float | T:
    if y == 0:
        raise ZeroDivisionError("Divisor cannot be 0")
    return x % y


type Function = Union[
    Callable[[int | float, int | float], int],
    Callable[[int | float, int | float], float],
    Callable[[int | float, int | float], Any],
]

operators: Dict[str, Function] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "%": modulus,
}


def main():
    print("=" * 50)
    print("PY CALCULATOR")
    print("=" * 50)
    try:
        x: float = float(input(" Number 1 >"))
        y: float = float(input(" Number 2 >"))
        # remove white spaces and only take the first value
        operator = str(input(" Operator (+,-,*,/,%) > ")).strip()[0]

        func = operators.get(operator, None)

        if not func:
            raise ValueError("Invalid operator.")

        result = func(x, y)

        print(f"\n{x: .2f} {operator} {y: .2f} = {result: .2f}\n")

    except Exception as e:
        print(f" X ERROR: {e}")


if __name__ == "__main__":
    main()
