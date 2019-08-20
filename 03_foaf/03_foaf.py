from library.group import Group

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

class Interests:
    pass



dump_group = Group(dump)
dump_group.analyze_friendships(friendship_pairs)
level = 2  # If level 0 is input here, then the function default values will be considered
print(f"The total number of connections in the dataset at level {level} is {dump_group.get_total_connections(level)}\n")
print(f"The person(s) most connected at level {level} is/are: \n "
      f"{[p.name for p in dump_group.get_most_connected_pers(level=level)]}\n")

# Show connections at the selected level
print(f"The connections that each person has at level {level} are:")
for k in range(len(dump)):
    conn_list = dump_group.get_person_by_id(k).get_connects(level=level)
    print(f"{dump_group.get_person_by_id(k).name} : {[p.name for p in conn_list]}")

# Suggest friends to each person of the group based on his friendships at the selected level
print("\nPersons from the Group that each person may know: ")
suggestions = dump_group.suggest_friends_each(level=1)
print(*[f"{dump_group.get_person_by_id(n).name} : {[p.name for p in suggestions[n]]}" for n in range(len(
    suggestions))], sep="\n")

# UNCOMMENT THIS  to compare the performances
    # TestPerformance.generate_data_and_test(100000)
