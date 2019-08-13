# This program will calculate the N-th Fibonacci number and, in order to test its performance, it will write the
# first 1000 number of Fibonacci serie.

import time

fibonacci_serie = {}

def fibonacci(n):
    # If this number has already been calculated, return it
    if n in fibonacci_serie:
        return fibonacci_serie[n]

    # Compute the value
    if type(n) != int or n < 0:
        print("The number you entered is not a valid integer")
    elif n == 0:
        result = 0
    elif n == 1 or n == 2:
        result = 1
    else:
        result = fibonacci(n-1)+fibonacci(n-2)

    # Store the result in the dictionary
    fibonacci_serie[n]=result
    return result

fibonacci_serie_iter = {}

def fibonacci_iter(n):

    if type(n) != int or n < 0:
        print("The number you entered is not a valid integer")
    elif n == 0:
        result = 0
    elif n == 1 or n == 2:
        result = 1
    else:
        # TODO: BE CAREFUL BECAUSE THE TWO METHODS CONSIDER DIFFERENTLY THE FIRST NUMBER 0
        # In one method 0 is the first number of the serie --> 499 is the 500th , in the other it is not
        result = 1
        two_prev = 0
        for i in range(n):
            if i in fibonacci_serie:
				# TODO memoization
            temp = result
            result = result + two_prev
            two_prev = temp
            print(result)
    fibonacci_serie_iter[n] = result
    return result
if __name__ == "__main__":
    start = time.time_ns()
    print(fibonacci_iter(8))
    print(time.time_ns()-start)

    # These following lines are interesting because they show that calculating only one number requires exactly the
    # same amount of time as calculating all the previous ones. This is the big advantage of "memoization" because
    # calculating the single number 500 requires generating all the fibonacci serie up to 500 through the previous 500
    # additions: 0+1+1+2+3+5+8+13+21+...
    # Similarly, calculating all the 500 numbers before requires generating the fibonacci serie up to 500 and storing
    # (and visualizing eventually) the partial results of the additions, but the number of operations is exactly the
    # same because the algorithm restarts the calculation exactly from where it left.

    # Of course running these lines and the previous ones in the same run does not make sense because at this line of
    # code the 500th Fibonacci's number has already been calculated, so fibonacci function would simply return the
    # stored value

    # start = time.time_ns()
    # for num in range(500):
    #     print(f"{num} = {fibonacci(num)}")
    # print(time.time_ns() - start)