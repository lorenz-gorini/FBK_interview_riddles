from .person import Person

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

