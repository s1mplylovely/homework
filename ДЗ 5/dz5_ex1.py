# 2 потока для вычисления квадратов и кубов целых чисел от 1 до 10
import threading


def square():
    for i in range(1, 11):
        print(f"{i}^2 = {i**2} ")


def cube():
    for i in range(1, 11):
        print(f"{i}^3 = {i**3} ")


t1 = threading.Thread(target=square)
t1.start()
t2 = threading.Thread(target=cube)
t2.start()
t1.join()
