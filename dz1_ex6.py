# 6 ValueError, ImportError
try:
    import math as m
    a = int(input())
    print(m.sqrt(a))
except ValueError:
    print("Ошибка: отрицательное число")
except ImportError:
    print("Ошибка: модуль не установлен")
