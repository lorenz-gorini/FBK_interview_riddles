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

fibonacci_serie_iter = {0:0,1:1,2:1}

def fibonacci_iter_mem(n):

    if type(n) != int or n < 0:
        print("The number you entered is not a valid integer")
    elif n == 0:
        result = 0
    elif n == 1 or n == 2:
        result = 1
    elif n <= max(fibonacci_serie_iter.keys()):
        return fibonacci_serie_iter[n]
    else:
        max_value_calculated = max(fibonacci_serie_iter.keys())
        result = fibonacci_serie_iter[max_value_calculated]
        two_prev = fibonacci_serie_iter[max_value_calculated-1]
        # TODO There are some good improvements but it is not fast yet. Maybe the difference is that... itereative
        #  functions are faster than for loop??? It is very strange!
        # It has to stop at n-1 if we consider 0 as the 0-th number of the serie, 1 as the 1st,
        # and the other 1 as the 2nd
        for i in range(max_value_calculated+1, n+1):
            # 1. assign to result the sum of the previous number of the fibonacci serie (result) and the value before
            # that
            # 2. assign the value of result to "two_prev" (i.e. the value before the previous one)
            two_prev, result = result, result + two_prev
            # store the new i-th value of the Fibonacci serie
            fibonacci_serie_iter[i] = result
    return result

def fibonacci_iter(n):

    if type(n) != int or n < 0:
        print("The number you entered is not a valid integer")
    elif n == 0:
        result = 0
    elif n == 1 or n == 2:
        result = 1
    else:
        # In one method 0 is the first number of the serie --> 499 is the 500th , in the other it is not
        result = 1
        two_prev = 0
        # It has to stop at n-1 if we consider 0 as the 0-th number of the serie, 1 as the 1st,
        # and the other 1 as the 2nd
        for _ in range(n-1):
            temp = result
            # summing the previous value of result and the value before that
            result = result + two_prev
            two_prev = temp
    return result

if __name__ == "__main__":
    start = time.time_ns()
    print(fibonacci_iter_mem(8))
    print(time.time_ns()-start)



    # These following lines are interesting because they show that calculating only one number requires exactly the
    # same amount of time as calculating all the previous ones. This is the big advantage of "memoization" because
    # calculating the single number 5000 requires generating all the fibonacci serie up to 5000 through the previous 5000
    # additions: 0+1+1+2+3+5+8+13+21+...
    # Similarly, calculating all the 5000 numbers before requires generating the fibonacci serie up to 5000 and storing
    # (and visualizing eventually) the partial results of the additions, but the number of operations is exactly the
    # same because the algorithm restarts the calculation exactly from where it left.

    # Of course running these lines and the previous ones in the same run does not make sense because at this line of
    # code the 5000th Fibonacci's number has already been calculated, so fibonacci function would simply return the
    # stored value

    start = time.time_ns()
    for num in range(5000):
        fibonacci_iter_mem(num)
        # print(f"{num} = {fibonacci(num)}")
    fib_iter_time = time.time_ns() - start
    print(fib_iter_time)

    start = time.time_ns()
    for num in range(5000):
        fibonacci(num)
    print(f"The ratio between the time of the algorithm with memoization and without it is :  "
          f"{(time.time_ns() - start)/fib_iter_time}")