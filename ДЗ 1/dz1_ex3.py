# 3 CustomError
class EvenError(Exception):
    pass


class NegativeError(Exception):
    pass


class EvenNegativeError(Exception):
    pass


def test_num(x):
    if (x % 2 == 0) and (x < 0):
        raise EvenNegativeError("Ошибка: четное отрицательное число в списке")
    elif x % 2 == 0:
        raise EvenError("Ошибка: четное число в списке")
    elif x < 0:
        raise NegativeError("Ошибка: отрицательное число в списке")
    else:
        pass


try:
    a = [int(x) for x in input().split()]
    for x in a:
        test_num(x)
    print(sum(a))
except EvenNegativeError as e:
    print(e)
except EvenError as e:
    print(e)
except NegativeError as e:
    print(e)
except ValueError:
    print("Ошибка: некорректный ввод")
