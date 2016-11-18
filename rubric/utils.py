from rubric.convertor import hierarchy

def fill_tree(tree):
    input_tree = tree.copy()
    input_tree.pop('submit')
    
    for node in input_tree:
        if input_tree[node] == '':
            input_tree[node] = fill_parent(node, input_tree)
        else:
            fill_children(node, input_tree)
    for ky in input_tree:
        if input_tree[ky] == '':
            input_tree[ky] = 0
    return input_tree

def fill_children(node, tree, graph=hierarchy.node_dict):
    """
    Gets all the children of the current node and fills them with the
    score of the node. 

    modifies the tree.
    """
    for child in graph[node]:
        tree[child] = tree[node]
        fill_children(child, tree)

def fill_parent(node, tree, graph=hierarchy.node_dict):
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
