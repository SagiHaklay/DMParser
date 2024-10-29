from vocabulary import Vocabulary
from earley import CFG, earley
from condition import check_condition

class DMParser:
    def __init__(self, syntax: CFG, vocabulary: Vocabulary) -> None:
        self.syntax = syntax
        self.vocabulary = vocabulary
        self.dm_cfg = CFG(syntax.start_var, vocabulary.phonological_values())
        for rule in syntax.rules:
            self.dm_cfg.add_rule(rule.left, rule.right)
        for terminal in syntax.get_terminals():
            vi = vocabulary.get_item(terminal)
            if vi is not None:
                for value, cond in zip(vi.values, vi.conditions):
                    self.dm_cfg.add_rule(terminal, [value], True, cond)

    def parse(self, phrase):
        result = False
        valid_trees = []
        earley_result, table  = earley(phrase, self.dm_cfg)
        if earley_result == False:
            return False, table
        for tree in table.get_trees(self.vocabulary.encoding):
            condition_nodes = [node for node in tree.leaves if node.condition != None]
            if all([check_condition(node, node.condition) for node in condition_nodes]):
                result = True
                valid_trees.append(tree)
        return result, table, valid_trees