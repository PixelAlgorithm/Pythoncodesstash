import random
def adder(size):
    return [random.random() for _ in range(size)]
def addition(x, y):
    adder(10**6)
    return x + y
x=int(input('Enter first number'))
y=int(input('Enter second number'))
result = addition(x, y)
print(f"The result of the addition is: {result}")
def result():
    while True:
        adder(10**6)

result()


