# 5 ValueError
try:
    a = float(input())
    print(a)
except ValueError:
    print("Невозможно преобразовать в число с плавающей точкой")
