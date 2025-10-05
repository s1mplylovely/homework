# 2 ValueError
try:
    a = int(input())
    b = int(input())
    print(a/b)
except ZeroDivisionError:
    print("Ошибка: деление на ноль")
except ValueError:
    print("Ошибка: некорректный ввод")
