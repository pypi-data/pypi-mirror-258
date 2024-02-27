# fibonacci_package/fibonacci.py

def calculate_fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Memoized version of the recursive Fibonacci algorithm
def fibonacci_with_memoization(n, cache={0: 0, 1: 1}):
    if n in cache:
        return cache[n]
    cache[n] = fibonacci_with_memoization(n - 1, cache) + fibonacci_with_memoization(n - 2, cache)
    return cache[n]
