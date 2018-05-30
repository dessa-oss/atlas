def traverse(fold_action, this_node):
    node_results = [traverse(fold_action, node) for node in this_node.previous_nodes()]
    return fold_action(node_results, this_node)

def lazy_traverse(fold_action, this_node):
    def node_results():
        for node in this_node.previous_nodes():
            yield lazy_traverse(fold_action, node)

    return fold_action(node_results(), this_node)

def force_results(lazy_iterable):
    return list(lazy_iterable)