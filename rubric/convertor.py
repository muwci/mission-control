import csv

from rubric.graph import Graph
from rubric.graph import Node

CORE_VALUES = "./rubric/data/PBDA-Core-Values.csv"

core_value_reader = csv.reader(open(CORE_VALUES))

header = next(core_value_reader)
criteria = [rw for rw in core_value_reader]

name_map = {}
hierarchy = Graph()

level_counters = {1:0, 2:0, 3:0}

for rw in criteria:
    if rw[1] not in name_map.values():
        level_counters[1] += 1
        level_counters[2] = 1
        level_counters[3] = 1
    else:
        if rw[2] not in name_map.values():
            level_counters[2] += 1
            level_counters[3] = 1
        else:
            level_counters[3] += 1
            
    nm1 = 'C' + str(level_counters[1])
    
    nm2 = 'C' + str(level_counters[1]) + \
                str(level_counters[2])
    
    nm3 = 'C' + str(level_counters[1]) + \
                str(level_counters[2]) + \
                str(level_counters[3])

    name_map[nm1] = rw[1]
    name_map[nm2] = rw[2]
    name_map[nm3] = rw[3]
    
    nd1 = Node(nm1)
    nd2 = Node(nm2)
    nd3 = Node(nm3)
    
    nd3.parent = nd2
    nd2.parent = nd1
    
    hierarchy.add_node(nd1)
    hierarchy.add_node(nd2)
    hierarchy.add_node(nd3)
