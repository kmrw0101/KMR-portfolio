"""Basic Python exercises for skill practice.

Add your Python exercises here for learning and skill development.
"""


# Exercise 1: Hello World
def hello_world():
    """Print a greeting."""
    print("Hello, World!")


# Exercise 2: Add two numbers
def add_numbers(a, b):
    """Return the sum of two numbers."""
    return a + b


# Exercise 3: Check if number is even
def is_even(n):
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


if __name__ == "__main__":
    hello_world()
    print(f"5 + 3 = {add_numbers(5, 3)}")
    print(f"4 is even: {is_even(4)}")
    print(f"7 is even: {is_even(7)}")
