import time


x = 0
while True:
    x += 1
    print(x)
    time.sleep(0.5)
    if x % 2 == 0:
        with open('log.txt', 'a') as f:
            f.write(str(x) + '\n')