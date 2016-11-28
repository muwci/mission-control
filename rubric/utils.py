from rubric.convertor import struct

def fill_tree(tree):    
    for node in tree:
        if tree[node] == '':
            tree[node] = fill_parent(node, tree)
        else:
            fill_children(node, tree)
    for ky in tree:
        if tree[ky] == '':
            tree[ky] = 0
    return tree

def fill_children(node, tree, graph=struct.node_dict):
    """
    Gets all the children of the current node and fills them with the
    score of the node. 

    modifies the tree.
    """
    for child in graph[node]:
        tree[child] = tree[node]
        fill_children(child, tree)

def fill_parent(node, tree, graph=struct.node_dict):
    """
    Takes the average of the weights of the children and assigns it to 
    the parent.

    modifies the tree.
    """
    if len(graph[node]) == 0:
        if tree[node] == '':
            return 0
        return int(tree[node])
    num_children = len(graph[node])
    total_sum = 0
    for child in graph[node]:
        if tree[child] == '':
            total_sum += fill_parent(child, tree)
        else:
            total_sum += int(tree[child])
    return int(round(total_sum/num_children))
