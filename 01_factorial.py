# This program calculates the factorial of a number

# This is the recursive algorithm
def factorial(n):
    if n == 1 or n == 0:
        return 1
    else:
        return n*factorial(n-1)

# This is the iterative algorithm
# I inserted here some checks before the calculus. If I had done that in the recursive function, those same checks
# would have been repeated over and over during the factorial calculation. There are some better ways to do that,
# like creating a different function for the checks, which calls the function with the algorithm only, for example.
def factorial_iter(n):
    if type(n)!=int or n<0:
        return "n is not a valid number"
    else:
        fact = 1
        for num in range(n):
            fact = fact * (n - num)
        return fact


if __name__ == "__main__":
    print(factorial_iter("a"))
    print(factorial_iter(7))
    print(factorial(7))
    print(factorial(0))
    print(7*6*5*4*3*2*1)