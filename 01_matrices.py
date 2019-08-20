# Write a program which takes 2 digits, i.e. M,N , and generates a matrix.
# The element value in the i-th row and j-th column of the matrix should be (i * j).
# Note: i = 0, 1, ..., M-1
#       j = 0, 1, ..., N-1
import collections
import time
import numpy as np


def insert_dimension(M, N):
    # This function gets the input of the 2 numbers which define the dimensions of a 2D matrix.
    # There are also some small checks and ways to get a correct value for every input.
    # If there are not 2 valuable numbers, it will return M=4, N=5

    # This is useful for time comparison (avoiding input time lag)
    if M and N:
        return M,N

    input_list = input("Please insert two digits which define the dimensions of a 2D matrix, like M,N \n")
    input_list += ','
    single_num, dim_matrix = [],[]
    poss_numbers = set([str(k) for k in list(range(10))])
    for l in input_list:
        # Everytime it finds a "," it aggregates the digits (found and stored previously) to form a number and it is
        # stored in the final results list (i.e. dim_matrix)
        if l == "," and single_num != []:
            single_num = int(''.join(single_num))
            dim_matrix.append(single_num)
            single_num = []
        if l in poss_numbers: single_num.append(l)
    if len(dim_matrix) < 2:
        print("You inserted a wrong number of values for the dimensions of the 2D-array. I choose 4,5")
        return 4,5
    return dim_matrix[:2]


# IMPLEMENTATION 1:
# Simple implementation with list-comprehension
def matrix_gen_simple(M = 0,N = 0):
    # This is just the simple version for time comparison
    M, N = insert_dimension(M,N)
    res_matrix = []
    basic_row = list(range(N))

    # Even though we may calculate the product of the basic_row and the scalar j element-wise to produce all the rows,
    # the map function is not really convenient performance-wise compared to the list-comprehension.
    for j in range(M):
        res_matrix.append([elem * j for elem in basic_row])

    return res_matrix


# IMPLEMENTATION 2:
# The two following functions are based on a different implementation I thought, that revealed to be 2x slower
# than the simple one. Particularly the first one is based on "deque" from the module "collections" and the second
# one is based on lists.
# The idea behind these implementations is to reduce the number of operations.
# Unfortunately I did some tests and I found that the big problem that takes away 80% of total computational time is
# appending new values to the matrix.
# Even though on lists and deque the "append" function has a complexity O(1), it is inserted in a double loop,
# which leads back to a complexity of O(M*N), but the list-comprehension of the simple case still gives an improvement.

# ALGORITHM: It can be noticed that if we cut the final matrix down to a squared one, this is symmetric.
# So this implementation calculates the rows/columns that are not in the squared matrix, and calculates only one
# half of the squared matrix. This theoretically may save some operations but it actually increased time.
# Number of memory accesses for the squared matrix:   O ( min(N,M) * min(N,M)/2 * 2 )
def matrix_gen_deque(M = 0, N = 0):
    M,N = insert_dimension(M, N)
    res_matrix = []
    square_mat_dim = min(N, M)
    basic_row = list(range(square_mat_dim))
    # Even though we may calculate the product of the basic_row and the scalar j element-wise to produce all the rows,
    # the map function is not really convenient performance-wise compared to the list-comprehension.
    # On the other hand, it can be noticed that if we cut the matrix down to a squared one, this is symmetric.
    # So we can calculate the rows/columns that are not in the squared matrix, and calculate only one half of the
    # squared matrix.

    # Generate the squared matrix
    # Create the first element
    res_matrix.append(collections.deque([0]))

    for row in range(1,square_mat_dim):
        # Create a new row in the matrix
        res_row = collections.deque()
        # Fill up the row and the column with the same values
        for elem in basic_row[:row]:
            value = elem * row
            # add the value to the new row
            res_row.append(value)
            # add the value to the old column
            res_matrix[elem].append(value)
        # This is adding the value on the diagonal (that is in common with row and column)
        res_row.append(basic_row[row]*row)
        res_matrix.append(res_row)

    # Generate the rows/columns that are not in the squared matrix
    rows_cols = []
    for row in range(abs(M - N)):
        res_row = [elem * (row + square_mat_dim) for elem in basic_row]
        rows_cols.append(res_row)

    # Append the rows/columns to the squared matrix, even though the extend function has a complexity O(n), where n is
    # the extension
    if M > N:
        res_matrix.extend(rows_cols)
    elif M < N:
        for i in range(M):
            res_matrix[i].extend([rc[i] for rc in rows_cols])

    return res_matrix


# IMPLEMENTATION 3:
# This is the same exact implementation done with lists
def matrix_gen_lists(M = 0, N = 0):
    M,N = insert_dimension(M, N)
    res_matrix = []
    square_mat_dim = min(N, M)
    basic_row = list(range(square_mat_dim))
    # Even though we may calculate the product of the basic_row and the scalar j element-wise to produce all the rows,
    # the map function is not really convenient performance-wise compared to the list-comprehension.
    # On the other hand, it can be noticed that if we cut the matrix down to a squared one, this is symmetric.
    # So we can calculate the rows/columns that are not in the squared matrix, and calculate only one half of the
    # squared matrix.

    # Generate the squared matrix
    # Create the first element
    res_matrix.append([0])

    for row in range(1,square_mat_dim):
        # Create a new row in the matrix
        res_matrix.append([])
        # Fill up the row and the column with the same values
        for elem in basic_row[:row]:
            value = elem * row
            # add the value to the new row
            res_matrix[row].append(value)
            # add the value to the old column
            res_matrix[elem].append(value)
        # This is adding the value on the diagonal (that is in common with row and column)
        res_matrix[row].append(basic_row[row]*row)

    # Generate the rows/columns that are not in the squared matrix
    rows_cols = []
    for row in range(abs(M - N)):
        res_row = [elem * (row + square_mat_dim) for elem in basic_row]
        rows_cols.append(res_row)

    # Append the rows/columns to the squared matrix, even though the extend function has a complexity O(n), where n is
    # the extension
    if M > N:
        res_matrix.extend(rows_cols)
    elif M < N:
        for i in range(M):
            res_matrix[i].extend([rc[i] for rc in rows_cols])

    return res_matrix


# IMPLEMENTATION 4:
# Finally, this implementation is based on numpy package.
def matrix_gen_numpy(M = 0,N = 0):
    # This is just the simple version for time comparison
    M, N = insert_dimension(M,N)
    # This numpy function creates two np.array that look like the indices of a grid M x N. So "i" will be a vertical
    # vector with M elements from 0 to M-1 and "j" will be a horizontal vector with N elements from 0 to N-1
    i,j = np.ogrid[:M,:N]
    # When I multiply the two np.array (1-dim) we get:  M*1 x 1*N  =  M*N   array
    # This multiplication is highly optimized
    res_matrix = i*j

    return res_matrix





if __name__ == "__main__":
    resulting_matrix = matrix_gen_numpy(4,5)
    print(''.join([f"{row}\n" for row in resulting_matrix]))

    # Time Comparison
    # SIMPLE VERSION
    start = time.time_ns()
    resulting_matrix_simple = matrix_gen_simple(2000, 2000)
    simple_time = time.time_ns() - start
    print(f"simple time: {simple_time}")

    # NUMPY VERSION
    start = time.time_ns()
    resulting_matrix_numpy = matrix_gen_numpy(2000, 2000)
    print(f"numpy/simple time ratio: {(time.time_ns() - start)/simple_time}")

    # DIFFERENT VERSION WITH DEQUE
    start = time.time_ns()
    resulting_matrix_deque = matrix_gen_deque(2000,2000)
    print(f"deque/simple time ratio: {(time.time_ns() - start)/simple_time}")

    # DIFFERENT VERSION WITH LISTS
    start = time.time_ns()
    resulting_matrix_lists = matrix_gen_lists(2000,2000)
    print(f"list/simple time ratio: {(time.time_ns() - start)/simple_time}")
