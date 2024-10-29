from anytree import AnyNode, find_by_attr

class Condition:
    def __init__(self, category, values, common=None) -> None:
        self.category = category
        self.values = values
        self.common = common

    def __repr__(self) -> str:
        return f"{self.category} in {self.values}"


def check_condition(node: AnyNode, condition: Condition):
    while not node.is_root and node.tag != condition.common:
        node = node.parent
    category_node = find_by_attr(node, name='tag', value=condition.category)
    if category_node is None or category_node.is_leaf:
        return False
    value_node = category_node.children[0]
    return value_node.tag in condition.values