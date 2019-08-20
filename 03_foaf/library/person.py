
class Person:
    def __init__(self, name: str, id_num: int):
        self.name = name
        self.id_num = id_num
        self.friends = set()
    def add_friend(self,friend):
        if friend.id_num != self.id_num:
            self.friends.add(friend)

    def get_connects(self, level=5):
        # This function is basically to separate the recursive algorithm from the function, that is meant to be called
        # Moreover there is not an easy way to remove the "self" element inside the recursive algorithm
        connects = self._get_indirect_connections_fast_2nd(level=level)
        connects.remove(self)
        return connects or []

    def _get_indirect_connections_fast_2nd(self, connections=None, level=5):
        """
        This recursive function gets all the connections at every level (default: 5) of this person.
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
        # First call of the recursive function --> First creation of the variable
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
                # recursively look for the friends of friends until you reach level=0 which means you got to the
                # desired level of indirect friendship.
                connections = f._get_indirect_connections_fast_2nd(connections=connections, level=level)

        return connections


    def get_indirect_conns_slow_no_lev(self, connections=None):
        """
        This recursive function gets all the connections at every level (default: 5) of this person.
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


    # A much simpler way, stopping at a specific level, was
    """
        most_connected = []
        max_conns_num = 0
        # This will be the variable we pass to the next steps of this recursive function eventually
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
        
    """
