def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(list(fibonacci(5)))
#for i in range(10):
 #   print(fibonacci(i))

#for num in fibonacci(10):
 #   print(num)