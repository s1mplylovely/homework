# 1 ZeroDivisionError
a = int(input())
b = int(input())
try:
    print(a/b)
except ZeroDivisionError:
    print("Ошибка: деление на ноль")
