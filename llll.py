import math

def validate_positive(func):
    def wrapper(x):
        if x <= 0:
            raise ValueError("Input must be a positive number")
        return func(x)
    return wrapper

@validate_positive
def square_root(x):
    return math.sqrt(x)

# Example usage:
try:
    result = square_root(25)
    print(result)  # Output: 5.0
except ValueError as e:
    print(e)

try:
    result = square_root(-4)
    print(result)
except ValueError as e:
    print(e)  # Output: Input must be a positive number