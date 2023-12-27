def module_tree(data_node) -> list:
    data = []
    for n in data_node:
        # 判断是否有子节点
        is_child = is_child_node(data_node, n)
        # 判断父节点为0且没有子节点
        if (n['parent_id'] == 0) and (is_child is False):
            data.append(n)
        # 判断父节点为0且有子节点
        elif (n['parent_id'] == 0) and (is_child is True):
            # 递归遍历父节点下的子节点
            res = node_tree(data_node, n)
            data.append(res)
    return data


def node_tree(nodes, current_node):
    """
    递归：获取节点的子节点
    """
    for node in nodes:
        if node['parent_id'] == current_node['id']:
            current_node['children'].append(node)
            node_tree(nodes, node)
    return current_node


def is_child_node(nodes, current_node):
    """
    判断当前字典是否有子节点
    """
    for node in nodes:
        # 判断是否节点的父id=当前节点id
        if node['parent_id'] == current_node['id']:
            return True
    return False
