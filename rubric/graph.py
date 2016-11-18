class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        
class Graph:
    def __init__(self):
        self.nodes = set()
        self.node_dict = {}
    
    def add_node(self, node):
        self.nodes.add(node)
        
        if not self.node_dict.get(node.name, None):
            self.node_dict[node.name] = set()

        if node.parent:
            self.node_dict[node.parent.name].add(node.name)
