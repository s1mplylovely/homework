# 4 IndexError
n = 10
a = [i for i in range(n)]
ind = int(input())
try:
    print(a[ind])
except IndexError:
    print("Ошибка индексации")
