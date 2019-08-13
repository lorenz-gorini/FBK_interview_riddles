# This program accepts a sequence of comma separated 6 digit binary numbers as its input,
# and then check whether they are divisible by 3 or not.
# Those binary numbers divisible by 3 should be printed in a comma separated sequence.

def find_divisible_numbers(divisor, base):
    single_num = [] # this will contain the single numbers
    resulting_list = []
    input_list = input("Please insert a sequence of comma separated binary numbers \n"
                       "NOTE: Everything that is not either 0 or 1 or ',' will be discarded and skipped\n")
    input_list +=','
    for l in input_list:
        if l == "," and single_num != []:
            result = 0
            for j in range(len(single_num)):
                result = result + int(single_num[j])*(base**(len(single_num)-j-1))
            if (result%divisor)==0:
                print(f"{result},", end = '')
            single_num = []
        if l == "0" or l == "1": single_num.append(l)
    return resulting_list

if __name__ == "__main__":
    results = find_divisible_numbers(3, 2)