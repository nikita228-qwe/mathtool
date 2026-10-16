"""mathtool — решение уравнений вида A*x^2 + B*x + C = 0 (консольное приложение)."""

import math
import sys

MAX_VALUE = 10000

HELP_TEXT = """mathtool — решение уравнений вида A*x^2 + B*x + C = 0

Использование:
    python mathtool.py                         вывод справки
    python mathtool.py --help                  вывод справки
    python mathtool.py solve                   ввод коэффициентов с клавиатуры
    python mathtool.py solve -a 1 -b -3 -c 2   решение с заданными коэффициентами

Коэффициенты A, B, C — целые числа, по модулю не превышающие 10000."""


def print_error(message):
    """Выводит сообщение об ошибке в стандартный поток ошибок."""
    print(message, file=sys.stderr)


def parse_arguments(args):
    """Разбирает параметры командной строки.

    Возвращает кортеж (команда, список строк с коэффициентами или None).
    Команда: 'help', 'input' или 'params'.
    """
    if not args or args[0] == "--help":
        return "help", None

    if args[0] != "solve":
        print_error("ОШИБКА: неизвестная команда, ожидается solve")
        sys.exit(1)

    if len(args) == 1:
        return "input", None

    if len(args) == 7:
        if args[1] != "-a" or args[3] != "-b" or args[5] != "-c":
            print_error("ОШИБКА: неизвестный параметр, ожидаются -a, -b, -c")
            sys.exit(1)
        return "params", [args[2], args[4], args[6]]

    print_error("ОШИБКА: неверный набор параметров")
    sys.exit(1)


def read_from_keyboard():
    """Запрашивает коэффициенты у пользователя и возвращает их как строки."""
    a_text = input("Введите A: ")
    b_text = input("Введите B: ")
    c_text = input("Введите C: ")
    return [a_text, b_text, c_text]


def convert_to_integers(texts):
    """Преобразует строки в целые числа. При ошибке завершает работу с кодом 1."""
    try:
        return [int(text) for text in texts]
    except ValueError:
        print_error("ОШИБКА: коэффициент не является целым числом")
        sys.exit(1)


def check_range(values):
    """Проверяет, что все коэффициенты не выходят за допустимый диапазон."""
    if any(abs(value) > MAX_VALUE for value in values):
        print_error("ОШИБКА: значение вне допустимого диапазона")
        sys.exit(1)


def solve_linear(b, c):
    """Решает линейное уравнение B*x + C = 0 при A = 0."""
    if b == 0:
        print_error("ОШИБКА: это не уравнение, неизвестное отсутствует")
        sys.exit(1)
    print("Уравнение линейное")
    x = -c / b + 0.0  # + 0.0 убирает знак минус у нуля
    print(f"x = {x:.10f}")


def solve_quadratic(a, b, c):
    """Решает квадратное уравнение A*x^2 + B*x + C = 0 при A != 0."""
    print("Уравнение квадратное")
    d = b * b - 4 * a * c
    print(f"D = {d}")

    if d > 0:
        root = math.sqrt(d)
        x1 = (-b + root) / (2 * a)
        x2 = (-b - root) / (2 * a)
        print(f"x1 = {x1:.3f}")
        print(f"x2 = {x2:.3f}")
    elif d == 0:
        x = -b / (2 * a) + 0.0
        print(f"x = {x:.3f}")
    else:
        print("Действительных корней нет")


def solve_equation(a, b, c):
    """Определяет вид уравнения и выводит решение."""
    if a == 0:
        solve_linear(b, c)
    else:
        solve_quadratic(a, b, c)


def main():
    command, texts = parse_arguments(sys.argv[1:])

    if command == "help":
        print(HELP_TEXT)
        sys.exit(0)

    if command == "input":
        texts = read_from_keyboard()

    a, b, c = convert_to_integers(texts)
    check_range([a, b, c])

    if a == 0 and b == 0:
        print_error("ОШИБКА: это не уравнение, неизвестное отсутствует")
        sys.exit(1)

    solve_equation(a, b, c)
    sys.exit(0)


if __name__ == "__main__":
    main()