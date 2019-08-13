"""
This is a program to sort the (name, topic, grade) tuples in ascending order,
where name and topic are string, grade is float.
The sorting criteria are:
1: topic
2: grade
3: name
Input tuples have to be provided via a CSV file that has to be read and processed
"""
name_file = "data_to_sort.csv"

def analyze_lines(lines):
    # Getting the actual data
    elaborated_lines = []
    for line in lines:
        name, topic, grade = "","",""
        line_data = [name, topic, grade]
        comma_count, i = 0, 0
        char = line[i]
        while comma_count < 3:
            while char != "," and char != "\n" and char != None:
                line_data[comma_count] += char
                i += 1
                char = line[i]
            # Skip some characters to get to the actual data
            while char == "," or char == " ":
                i += 1
                char = line[i]
            comma_count += 1
        line_data[2] = float(line_data[2])
        """
        # The following lines will not be used because we use the casting from string to float for the "grade" variable
        if comma_count == 2:
            floating_point = False
            for num in line[i:]:
                if num == ".":
                    floating_point = True
                elif num == "\n" or num == " ":
                    continue
                else:
                    if floating_point:
                        line_data[comma_count] = line_data[comma_count] + int(num)/10
                    else:
                        line_data[comma_count] = line_data[comma_count]*10 + int(num)
        """
        # Since Python simply add a reference to line_data and it does not use more memory for instantiating a copy,
        # the "elaborated_data" variable can be used instead of using "line_data" as a 2D array which would make
        # the previous lines less readable
        elaborated_lines.append(line_data)
    return elaborated_lines

def readfile(name_file):
    # Reading File
    f = open(f"./{name_file}", "r")
    if f.mode == 'r':
        lines = f.readlines()
        data = analyze_lines(lines)
        return data
    else:
        print("File not found or not readable")

def sort_data_simple_slow(students, order_by):
    """
    OPTION 2: Simple sort
    This version of the algorithm compares all the elements 1 by 1 for three times (the number of variables for every
    element according to which they have to be sorted)  --> Complexity O( 3* N^2)
    COMMENT: There are many ways to improve this algorithm in order to avoid the 3 factor. For example when we find
    some elements which are the same, we could append them to a list in order to sort only them, without going
    through all the elements two other times.
    Similarly, but in a different way, Bubble Sort algorithm stop the comparisons whenever it notices there are no more
    changes in the list
    By the way none of these methods would change the N^2 factor which increases very fast with data.
    """
    for _ in order_by:
        for i in range(len(students[:-1])):
            for j in range(len(students[(i+1):])):
                ord = 0
                while students[i][order_by[ord]] == students[j+i+1][order_by[ord]]: # ord != 3 and
                    ord +=1
                if ord == 3:
                    print(f"There are two students {students[i]} and {students[j+i+1]} who are exactly the same. The "
                          f"data is "
                          f"repeated. I suggest to delete it from the data file")
                    continue
                else:
                    if students[i][order_by[ord]]>students[i+j+1][order_by[ord]]:
                        temp = students[i][order_by[ord]]
                        students[i][order_by[ord]] = students[i+j+1][order_by[ord]]
                        students[i+j+1][order_by[ord]] = temp
    return students

class Merge_Algorithm:
    """
    Having a class, instead of a bunch of functions, allows me to share some variables defined in the __main__ function
    over all the sorting functions of the class.
    The sorting algorithm is inspired by the "merge_sort" algorithm, which has already proved to be very solid and fast
    with a complexity of order O(N log N).
    Particularly this algorithm needs to split all the list down to single elements in order to build it up again in
    an ordered way. On the other hand Python does not use more memory to create new variables or smaller lists,
    but it only adds new references to those variables.

    Differently from the previous algorithm, we don't need to run the algorithm three times, for each column we want
    to sort the list. In this case we are using a recursive function which puts together two ordered lists, so
    whenever it finds two elements with the same value of the first column to sort, it uses the second column to find
    the correct order. After that comparison, we can be sure that the following comparisons between elements with the
    same values of the first column will be only for higher values of the second column, because the two lists we are
    merging are already ordered.

    To calculate the complexity and the number of comparisons, we understand that every list is split in half,
    and then they are being put together again with the same elements but in an ordered way.
    When they are being put together the number of comparisons are the same as the "number of elements of the
    resulting list "(because every comparison needs one new element of one of the two sub-lists and because
    the lists are split in half so they have the same number of elements) -2 ( or -3 for the single sub-list
    at the end of a list with an odd number of elements. This -2 is due to the last element which is not compared with
    anything but only added to the resulting list, and it is due to the first comparison which needs two new elements).
    So we will have:
     N/2*(2-1) comparisons when the sublists are only composed of one element and the resulting list is made of two.
                (this is the only case where we find -1 instead of -2 or -3)
     N/4*(4-2)
     N/8*(8-2)
     ...
    So this is a sum over k that goes from 2 to L of the function  [N/(2^i) * (2^i-2)] , where L solves 2^L=N,
    meanly L=log_2(N). To this sum we will add +N/2.
    What we want to prove is that this sum is similar to N*log(N) for N -> +inf . The calculation does not look
    really great and understandable if written like this, so I will continue in the README file

    CONCLUSION:
    This is a significant improvement compared to the Simple Algorithm I wrote above where the complexity is
    O(3*N^2).
    """

    def __init__(self, order_by):
        self.order_by = order_by

    def merge(self, left, right):
        result = []
        left_idx, right_idx = 0, 0
        while left_idx < len(left) and right_idx < len(right):
            col = 0
            # If the algorithm finds two students with the same value of the first variable we want to use to sort them,
            # it will use the value of the second (or more if needed) to find the correct order
            while left[left_idx][self.order_by[col]] == right[right_idx][self.order_by[col]]:
                if col == 2:
                    print(f"There are two students {[left[left_idx]]} at lines {left[left_idx]} and "
                          f"{right[right_idx]} of the file who are exactly the same. The data may be repeated. I suggest "
                          f"to delete one from the data file")
                    break
                col += 1

            # change the direction of this comparison to change the direction of the sort
            if left[left_idx][self.order_by[col]] <= right[right_idx][self.order_by[col]]:
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1
        # Understand which condition made the algorithm exit from the while loop. If one of the two lists is finished,
        # the other one still contains some elements which need to be added to the result
        if left_idx < len(left):
            result.extend(left[left_idx:])
        if right_idx < len(right):
            result.extend(right[right_idx:])
        return result

    def merge_sort(self, m):
        """
        This recursive function keeps splitting up the list (received as argument) in a left part and a right part until
        the two parts are composed of one element only.
        """
        if len(m) <= 1:
            return m

        # Splitting the list in half
        middle = len(m) // 2
        left = m[:middle]
        right = m[middle:]

        # Repeat the previous steps until the list is made of one element only.
        # Then, starting from the one element lists (last called), we start to merge them together in an ordered
        # list by executing the following line
        left = self.merge_sort(left)
        right = self.merge_sort(right)
        # Merge the two ordered list (the lowest level one element list are already ordered) into a new ordered list
        list_temp = list(self.merge(left, right))
        return list_temp


if __name__ == "__main__":
    students = readfile(name_file)
    order_by_criteria = (1, 2, 0)

    assert len(students[0]) == len(order_by_criteria), "The selected 'order by' criteria has a size different from " \
                                                       "the number of columns of the data"
    # Option 1: SLOWER
    # sort_data_2(students, order_by_criteria)

    # Option 2: FASTER
    mer = Merge_Algorithm(order_by_criteria)
    sorted_data = mer.merge_sort(students)
    print(sorted_data)



    # # THESE ARE SOME RANDOM THOUGHTS ABOUT THE COMPLEXITY AND INITIAL DRAFTS OF DIFFERENT IMPLEMENTATIONS I TRIED

    # # OPTION C:
    # def elem_to_be_considered_func(column):
    #     column = column
    #
    #     def elem_to_be_considered(element):
    #         return element[column]
    #
    #     return elem_to_be_considered
    #
    # def sort_data_2(students, order_by):
    #     """
    #     OPTION 2: Simple sort
    #     This version of the algorithm compares all the elements 1 by 1 for three times (the number of variables for every
    #     element according to which they have to be sorted)  --> Complexity O( 3* N^2)
    #     """
    #     for ord in [1]:  # order_by:
    #         students.sort(key=elem_to_be_considered_func(ord))
    #     return students

    # # OPTION D:
    # """
    #     ASSUMPTION: We need to order the elements according to the topic as priority.
    #     Looking at the data structure, it can be noticed that the topics are a small number, so I assume they are at
    #     least an order of magnitude less than the elements.
    #     If I had to order the students according to the grade, (which is allowed) this would make the algorithm very
    #     inefficient
    #
    #     OPTION 1: Sorting the categories (topics in our case)
    #     a. I get all the possible categories, and I create a set (operation of complexity O(N) )
    #     b. Order the categories (complexity O(C log C) if done with the Python function sort() , but in this case C
    #         is the number of categories instead of all the elements)
    #     c. The list is not ordered but I have to go through that for each category to compare only the elements of that
    #         category (complexity O(C*N) )
    #
    #         IMPLEMENTATION DRAFT:
    #         first_lev_categories = set([row[order_by[0]] for row in students])
    #         first_lev_categories = sorted(first_lev_categories)
    #         for first_cat in first_lev_categories:
    #             for stud in students:
    #
    #     OPTION 2: Sorting the elements by category (topic in our case)
    #     a. Order the elements by category (complexity O(N log N) where N is the number of elements)
    #     b. Order the elements of the same category (I can go through all the list of students, taking care of the
    #     change in category)
    #
    #     CHOICE: I need to decide if there are a lot of categories C or just a limited number of them, so the value of
    #     C log C + (C+1)*N < N log N .  In order to get an idea, if we have a number of elements = 1000 (or 10000),
    #     the categories need to be no more than 6 (or 8), in order to make OPTION 1 more convenient than OPTION 2.
    #     For these reasons I assume OPTION 2 is more convenient.
    #
    #     NOTE: Everything would be different if I had to use a very simple sort algorithm were the complexity is O(
    #     N^2), and in that case the OPTION 1 would be much more convenient.
    # """
    # sorted_students = []
    # categories = set()
    # index_new_categories = []
    # elem_ids_by_category = []
    # for stud in students:
    #     # Since it is a set (hashed), the complexity of the following check is O(1)
    #     if stud[order_by[0]] not in categories:
    #         categories.add(stud[order_by[0]])
    #     elem_ids_by_category[stud[order_by[0]]].append(students.index(stud))
    # # We assume the categories are limited, so the following line has a limited complexity O(C log C)
    # sorted_categories = sorted(categories)
    #
    # return sorted_students