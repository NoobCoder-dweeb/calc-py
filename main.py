# Additionally, this project uses python generics
from typing import TypeVar, Dict, Callable, Union
from pathlib import Path
import asyncio

T = TypeVar("T", bound=float)
FILE_PATH: Path = Path("./calcs.txt")


class Stack[T]:
    """
    Data Structure that contains calculations made in the past in string
    """

    def __init__(self) -> None:
        print("\nInitialising stack...")
        self.items: list[T] = []
        self.size: int = 0

    def push(self, x: T) -> None:
        self.items.append(x)
        self.size += 1

    def pop(self) -> T:
        self.size -= 1
        return self.items.pop()

    def peek(self) -> T:
        return self.items[-1]

    def len(self) -> int:
        return self.size

    def __sizeof__(self) -> int:
        return self.len()


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
    Callable[[int | float, int | float], None],
]

operators: Dict[str, Function] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "%": modulus,
}

stack = Stack[str]()


async def load_files():
    try:
        with open(FILE_PATH, "r") as f:
            for item in f:
                stack.push(item)
                await asyncio.sleep(0.001)

        # reverse the ordering because saved in LIFO
        stack.items = stack.items[::-1]

    except FileNotFoundError:
        return


async def save_progress():
    if stack.len == 0:
        return
    print("\nSaving progress...")
    try:
        with open(FILE_PATH, "w") as f:
            while stack.len() > 0:
                f.write(stack.pop())
                await asyncio.sleep(0.001)

    except FileNotFoundError:
        return


def compute() -> None:
    x: float = float(input(" Number 1> "))
    y: float = float(input(" Number 2> "))
    # remove white spaces and only take the first value
    operator = str(input(" Operator (+,-,*,/,%) > ")).strip()[0]

    func = operators.get(operator, None)

    if not func:
        raise ValueError("Invalid operator.")

    result = func(x, y)

    print(f"\n{x: .2f} {operator} {y: .2f} = {result: .2f}\n")
    stack.push(f"{x: .2f} {operator} {y: .2f} = {result: .2f}\n")


async def main():
    await load_files()

    print("=" * 50)
    print("PY CALCULATOR")
    print("=" * 50)
    while True:
        try:
            print("Choices:")
            print(" 1) Calculate")
            print(" 2) Last Calculation")
            print(" 3) Quit")

            choice: int = int(input(" Choice> "))

            match choice:
                case 1:
                    compute()
                case 2:
                    print(f"\n{stack.peek()}")
                case 3:
                    break
                case _:
                    raise ValueError(f"{choice} is not valid")

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f" X ERROR: {e}")

    await save_progress()


if __name__ == "__main__":
    asyncio.run(main())
