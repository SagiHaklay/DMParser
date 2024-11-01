from anytree import AnyNode, find_by_attr

class Condition:
    def __init__(self, category, values, common=None, is_elsewhere=False) -> None:
        self.category = category
        self.values = values
        self.common = common
        self.is_elsewhere = is_elsewhere

    def __repr__(self) -> str:
        if self.is_elsewhere:
            return f"Elsewhere: {self.category} not in {self.values}"
        return f"{self.category} in {self.values}"
    

def get_conditions(category, value_lists, common=None, with_elsewhere=False):
    conditions = [Condition(category, values, common) for values in value_lists]
    if with_elsewhere:
        elsewhere_vals = [val for values in value_lists for val in values]
        conditions.append(Condition(category, elsewhere_vals, common, True))
    return conditions


def check_condition(node: AnyNode, condition: Condition):
    while not node.is_root and node.tag != condition.common:
        node = node.parent
    category_node = find_by_attr(node, name='tag', value=condition.category)
    if category_node is None or category_node.is_leaf:
        return False
    value_node = category_node.children[0]
    if condition.is_elsewhere:
        return value_node.tag not in condition.values
    return value_node.tag in condition.values