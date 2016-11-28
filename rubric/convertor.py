import csv

from rubric.graph import Graph
from rubric.graph import Node

CRITERIA_DATA = [ 
    ('A', "./rubric/data/PBDA-Academic-and-Research.csv"),
    ('B', "./rubric/data/PBDA-Learning-and-Innovation.csv"),
    ('C', "./rubric/data/PBDA-21st-Century-Themes.csv"),
    ('D', "./rubric/data/PBDA-Information-Communication-Media-and-Tech.csv"),
    ('E', "./rubric/data/PBDA-Life-and-Career.csv"),
    ('F', "./rubric/data/PBDA-Core-Values.csv")
]

rubric_name_map = {}
struct = Graph()

for criteria_id, criteria_file in CRITERIA_DATA:    
    criteria_reader = csv.reader(open(criteria_file))
    criteria = [rw for rw in criteria_reader]

    level_counters = {1:0, 2:0, 3:0}

    for rw in criteria:
        if rw[1] not in rubric_name_map.values():
            level_counters[1] += 1
            level_counters[2] = 1
            level_counters[3] = 1
        else:
            if rw[2] not in rubric_name_map.values():
                level_counters[2] += 1
                level_counters[3] = 1
            else:
                level_counters[3] += 1
                
        nm0 = criteria_id

        nm1 = criteria_id + str(level_counters[1])
        
        nm2 = criteria_id + str(level_counters[1]) + \
                            str(level_counters[2])
        
        nm3 = criteria_id + str(level_counters[1]) + \
                            str(level_counters[2]) + \
                            str(level_counters[3])

        rubric_name_map[nm0] = rw[0]
        rubric_name_map[nm1] = rw[1]
        rubric_name_map[nm2] = rw[2]
        rubric_name_map[nm3] = rw[3]
        
        nd0 = Node(nm0)
        nd1 = Node(nm1)
        nd2 = Node(nm2)
        nd3 = Node(nm3)
        
        nd3.parent = nd2
        nd2.parent = nd1
        nd1.parent = nd0
        
        struct.add_node(nd0)
        struct.add_node(nd1)
        struct.add_node(nd2)
        struct.add_node(nd3)

for n, k in enumerate(sorted(ky for ky in rubric_name_map.keys() if len(ky) != 1)):
    if n%4 == 0:
        print('')
    print(str(k) + ' integer, ', end='')
