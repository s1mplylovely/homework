# Несколько потоков для функции, которая выводит целые числа от 1 до 10 с задержкой в 1 секунду
import threading
import time


def nums(thread):
    for i in range(1, 11):
        print(f"Поток № {thread}: {i}")
        time.sleep(1)


threads = []
n = 3

for i in range(1, n+1):
    thread = threading.Thread(target=nums, args=(str(i),))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
