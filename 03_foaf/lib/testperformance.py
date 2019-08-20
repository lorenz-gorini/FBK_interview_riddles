import random
import string
import sys
import time

# sys.path.append('../')
# import Group

class recursionlimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)


class TestPerformance:
    """
    These following static methods have been used to test the performances of the two algorithms:
    With 100 people and 50 friendship_pairs, the performances are very similar, but with 10000 and 5000 of them,
    the fast algorithm is 6-10x faster. This factor is due to the limited search in the fast algorithm.
    """

    @staticmethod
    def randomString(stringLength=5):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(stringLength))

    @staticmethod
    def generate_data_and_test(big_num_people=100000):
        random.seed(1)
        bigger_dump = [(TestPerformance.randomString(7), i) for i in range(big_num_people)]
        bigger_friendship_pairs = [(random.randint(0, big_num_people - 1), random.randint(0, big_num_people - 1)) for _
                                   in
                                   range(50000)]

        with recursionlimit(2000):
            dump_group = Group(bigger_dump)
            dump_group.analyze_friendships(bigger_friendship_pairs)
            start_time = time.time_ns()
            for k in range(100):
                conn_list = dump_group.get_person_by_id(k).get_indirect_connections_fast_2nd()
                print(len(conn_list), end="\t")  # To compare the results
            fast_time = time.time_ns() - start_time

            print("Slow algorithm results:")
            start_time = time.time_ns()
            for k in range(100):
                conn_list = dump_group.get_person_by_id(k).get_indirect_conns_slow_no_lev()
                print(len(conn_list), end="\t")  # To compare the results
            slow_time = (time.time_ns() - start_time)
            print(f"\nFast time is: {fast_time}")
            print(f"Slow time is: {slow_time}")
            print(f"Slow vs. fast algorithms time ratio is {slow_time / fast_time}")