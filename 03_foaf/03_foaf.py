
from lib.testperformance import TestPerformance

"""
Regarding the data structure I may have some options:
- list where the indexes are ids (None if the index is not among the possible ids listed in dump)
- I choose to have classes because they are more flexible to add further informations about the Person, 
like for example what the Person likes (useful in the second part of the exercise)
"""

dump = [('Hero', 0), ('Dunn', 1), ('Sue', 2), (3, 'Chi'),
 (4, 'Thor'), (5, 'Clive'), ('Hicks', 6),
 ('Devin', 7), ('Mate', 8), (9, 'Klein'),
 (10, 'Pen'), ('Cleven', 11)]

friendship_pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 4),
                    (3, 4), (4, 5), (3, 1), (5, 6), (5, 1), (5, 7),
                    (1, 0), (13, 2), (8, 9), (7, 8), (6, 8), (4, 4),
                    (8, 6), (2, 1), (3, 1), (10, 7), (9, 5), (5, 19),
                    (12, 4), (11, 11), (8, 5), (3, 0), (4, 1)]

interests = [
    (0, "Map-Reduce"), (0, "Data Lake"), (0, "Columnar Database"), (0, "Java"),
    (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"), (1, "Python"),
    (2, "Python"), (2, "scikit-learn"), (2, "scipy"), (2, "numpy"),
    (2, "numerical computation"), (2, "pandas"), (2, "big data"),
    (3, "R"), (3, "Python"), (3, "statistics"), (3, "regression"),
    (3, "scientific computation"), (3, "mathematics"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (4, "classification"), (4, "cross validation"),
    (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (5, "Data science"),
    (6, "statistics"), (6, "probability"), (6, "mathematics"), (6, "theory"),
    (6, "science"), (6, "software engineering"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (7, "machine learning"), (7, 'TensorFlow'),
    (8, "Big Data"), (8, "Map Reduce"), (8, "artificial intelligence"),
    (9, "Hadoop"), (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]



class Person:
    def __init__(self, name: str, id_num: int):
        self.name = name
        self.id_num = id_num
        self.friends = set()
    def add_friend(self,friend):
        if friend.id_num != self.id_num:
            self.friends.add(friend)

    def get_connects(self, level=5):
        # This function is basically to separate the iterative algorithm from the function, that is meant to be called
        # Moreover there is not an easy way to remove the "self" element inside the iterative algorithm
        connects = self._get_indirect_connections_fast_2nd(level=level)
        connects.remove(self)
        return connects or []

    def _get_indirect_connections_fast_2nd(self, connections=None, level=5):
        """
        This iterative function gets all the connections at every level (default: 5) of this person.
        The level of indirect connections measures how close the friends are.
        E.g. a friend = level 1
             a friend of a friend = level 2
             a friend of a friend of a friend = level 3
             ...
        The connections variable contains the connections we already know about the Person.
        The default value is None
        :return: list[Person]
        """
        level = level - 1
        # First call of the iterative function --> First creation of the variable
        if connections == None:
            connections = set([self])

        # This generates the list of friends who will be analyzed in the loop
        friends_still_to_search = set([x for x in self.friends if x not in connections])
        # Once every friend of the Person has already been analyzed (or he will be in later cycles), we can stop and
        # return the connections we found so far
        if friends_still_to_search == set():
            return connections
        # It adds all the friends who will be analyzed for connections.
        # Infact connections must contain also the people who will be analyzed in later cycles while being in the loop
        connections = connections | friends_still_to_search

        if level != 0:
            for f in friends_still_to_search:
                # Iteratively look for the friends of friends until you reach level=0 which means you got to the
                # desired level of indirect friendship.
                connections = f._get_indirect_connections_fast_2nd(connections=connections, level=level)

        return connections


    def get_indirect_conns_slow_no_lev(self, connections=None):
        """
        This iterative function gets all the connections at every level (default: 5) of this person.
        The level of indirect connections measures how close the friends are.
        E.g. a friend = level 1
             a friend of a friend = level 2
             a friend of a friend of a friend = level 3
             ...
        The connections variable contains the connections we already know about the Person.
        The default value is None
        :return: list[Person]
        """
        # Create the connections only if it is the first call
        if connections == None:
            # The addition of the "self" element at the set is preventing the other friends to select this as a
            # friend, which would start the search for its friends again
            connections = set()
        friends_still_to_search = [x for x in self.friends if x not in connections]
        # Once all the friends of the "self" Person are already in connections, "connections" can be returned
        if friends_still_to_search == []:
            return connections

        # For every friend that are not inserted in "connections" yet, we look for their connections to find all the
        # possible indirect friendships
        for f in friends_still_to_search:
            connections.add(f)
            for p in f.get_indirect_conns_slow_no_lev(connections):
                connections.add(p)
        return connections

    def suggest_friend(self, level=1):
        # This is a function to suggest possible other person that this Person self might know
        # This simply gets the connections of consecutive levels and compares them
        second_lv_connects = self.get_connects(level=level+1)
        first_lv_connects = self.get_connects(level=level)
        friend_suggestions = [f for f in second_lv_connects if f not in first_lv_connects]
        return friend_suggestions


class Group:
    """
    This class gathers all the properties and useful methods to manage a list of Persons with a relation of friendships
    """
    def __init__(self, dump):
        self.group = {}
        for p in dump:
            first, second = p
            if isinstance(first, int):
                id_num = first
                name = second
            else:
                id_num = second
                name = first
            self.group[id_num] = Person(name, id_num)

    def get_person_by_id(self, id):
        if id in self.group:
            return self.group[id]
        print(f"None person has {id}")
        return None

    def analyze_friendships(self, friendship_pairs):
        for p in friendship_pairs:
            p1, p2 = p
            if p1 in self.group and p2 in self.group and p1 != p2:
                self.get_person_by_id(p1).add_friend(self.get_person_by_id(p2))
                self.get_person_by_id(p2).add_friend(self.get_person_by_id(p1))
            else: print("There is a friendship_pair with non-existing ids. Please check. Skipped pair")

    def get_total_connections(self, level=3):
        # This function returns the number of total connections in the dataset, depending on the level you input
        total_connects = 0
        for id in self.group:
            total_connects += len(self.get_person_by_id(id).get_connects(level=level))
        return total_connects

    def get_most_connected_pers(self, level=1000, people_to_analyze=None):
        """
        Assuming every person and friendship is equally valuable from our point of view, the most connected person is
        the one who has the most friends. If there is a draw, we go to lower level friendship, meanly the more indirect
        friendships.
        It is worth noting that for very low indirect friendship, there will be some groups who are all interconnected
        in indirect ways, and completely isolated from the rest of the group. This means that in this case there is
        not a most connected person at that level. If wanted, we should stop at a higher level (so this is an
        argument of the function).
        For these reasons, starting with a low value of the "level" variable is highly suggested.

        A much simpler way, stopping at a specific level, was
        """
        most_connected = []
        max_conns_num = 0
        # This will be the variable we pass to the next steps of this iterative function eventually
        if people_to_analyze == None:
            people_to_analyze = self.group

        for id_num in people_to_analyze:
            connections = self.get_person_by_id(id_num).get_connects(level=level)
            # If there is a new max in connections, we reset the "most_connected" list
            if len(connections) > max_conns_num:
                max_conns_num = len(connections)
                most_connected = [(id_num, connections)]
            # If there is a draw, we just append the other person
            elif len(connections) == max_conns_num:
                most_connected.append((id_num,connections))
        # Now we need to check if the "most connected" are friends of each other, because in that case it means we
        # are in a subgroup where everybody is connected. (in that case moving to lower levels does not help)
        if len(most_connected) != 1:
            check = True
            # Check if the most_connected people are friends to each other (to the first one for example)
            # Since they are set, the computation time is equal to the time required to hash the value
            friend_ids = set([p.id_num for p in most_connected[0][1]])
            for i in range(1,len(most_connected)):
                print(check)
                check = check and (most_connected[i][0] in friend_ids)

            if check: return [self.get_person_by_id(m) for m,_ in most_connected]

        # If there is a draw among some persons, we go to lower levels
        if len(most_connected) != 1:
            level = level + 1
            print(level)
            most_connected = self.get_most_connected_pers(people_to_analyze=[m for m,_ in most_connected], level=level)

        return [self.get_person_by_id(m) for m,_ in most_connected]

    def suggest_friends_each(self, level=1):
        friend_suggestions = []
        for id in self.group:
            friend_suggestions.append(self.get_person_by_id(id).suggest_friend(level=level))
        return friend_suggestions


class Interests:
    pass


if __name__ == "__main__":

    dump_group = Group(dump)
    dump_group.analyze_friendships(friendship_pairs)
    print(f"The total number of connections in the dataset is {dump_group.get_total_connections(2)}")
    print(f"The person(s) most connected is/are: \n {[p.name for p in dump_group.get_most_connected_pers(level=2)]}")
    # Show connections at the selected level
    for k in range(len(dump)):
        conn_list = dump_group.get_person_by_id(k).get_connects(level=2)
        print(f"{dump_group.get_person_by_id(k).name} : {[p.name for p in conn_list]}")
    # Suggest friends to each person of the group based on his friendships at the selected level
    print("Persons from the Group that each person may know: ")
    suggestions = dump_group.suggest_friends_each(level=1)
    print([f"{dump_group.get_person_by_id(n).name} : {[p.name for p in suggestions[n]]}\n" for n in range(len(
        suggestions))])

    # TestPerformance.generate_data_and_test(100000)




    # def get_indirect_connections_fast(self, f_already_analyzed=None, connections=None, level=5):
    #     """
    #     This iterative function gets all the connections at every level (default: 5) of this person.
    #     The level of indirect connections measures how close the friends are.
    #     E.g. a friend = level 1
    #          a friend of a friend = level 2
    #          a friend of a friend of a friend = level 3
    #          ...
    #     The connections variable contains the connections we already know about the Person.
    #     The default value is None
    #     :return: list[Person]
    #     """
    #     # First call of the iterative function --> First creation of the variable
    #     if f_already_analyzed == None:
    #         f_already_analyzed = set()
    #     # If the Person's friends have already been analyzed, return connections
    #     if self in f_already_analyzed:
    #         # one not returning connections
    #         return connections, f_already_analyzed
    #     # I append the Person I am going to analyze
    #     f_already_analyzed.add(self)
    #     # Create the connections only if it is the first call
    #     if connections == None:
    #         # The addition of the "self" element at the set is preventing the other friends to select this as a
    #         # friend, which would start the search for its friends again
    #         connections = set()
    #     friends_still_to_search = [x for x in self.friends if x not in f_already_analyzed]
    #
    #
    #     # The iterative search can be a bit repetitive because it looks for every friend of every friend iteratively
    #     # until .
    #
    #     # For every friend that are not inserted in "connections" yet, we look for their connections to find all the
    #     # possible indirect friendships
    #     for f in friends_still_to_search:
    #         connections.add(f)
    #         # This variable describes the other friends who will be searched in the following loops
    #         other_friends = friends_still_to_search.remove(f)
    #         connections, f_already_analyzed = f.get_indirect_connections_fast(f_already_analyzed=f_already_analyzed,
    #                                                                           connections=connections)
    #         for p in [x for x in connections if x not in f_already_analyzed]:
    #             connections.add(p)
    #     return connections, f_already_analyzed

    # def get_indirect_connections(self, connections=None, level=5):
    #     """
    #     This iterative function gets all the connections at every level (default: 5) of this person.
    #     The level of indirect connections measures how close the friends are.
    #     E.g. a friend = level 1
    #          a friend of a friend = level 2
    #          a friend of a friend of a friend = level 3
    #          ...
    #     The connections variable contains the connections we already know about the Person.
    #     The default value is None.
    #     :return: list[Person]
    #     """
    #     # Whenever the function is called
    #     # level = level - 1
    #     # Create the connections only if it is the first call
    #     if connections == None:
    #         # The addition of the "self" element at the set is preventing the other friends to select this as a
    #         # friend, which would start the search for its friends again
    #         connections = set()
    #     friends_still_to_search = [x for x in self.friends if x not in connections]
    #     # Once all the friends of the "self" Person are already in connections, "connections" can be returned
    #     if friends_still_to_search == []:
    #         return connections, level
    #
    #     # For every friend that are not inserted in "connections" yet, we look for their connections to find all the
    #     # possible indirect friendships
    #     for f in friends_still_to_search:
    #         connections.add(f)
    #         if level != 0:
    #             conn_list, level = f.get_indirect_connections(connections, level - 1)
    #             for p in conn_list:
    #                 connections.add(p)
    #     return connections, level