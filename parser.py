from vocabulary import Vocabulary
from earley import CFG, earley, earley_by_word_lattice
from condition import check_condition
from word_splitter import create_word_lattice

class DMParser:
    def __init__(self, syntax: CFG, vocabulary: Vocabulary) -> None:
        self.syntax = syntax
        self.vocabulary = vocabulary
        self.dm_cfg = CFG(syntax.start_var, vocabulary.phonological_values())
        for rule in syntax.rules:
            self.dm_cfg.add_rule(rule.left, rule.right, cond=rule.condition)
        for terminal in syntax.get_terminals():
            vi = vocabulary.get_item(terminal)
            if vi is not None:
                for value, cond in zip(vi.values, vi.conditions):
                    self.dm_cfg.add_rule(terminal, [value], True, cond)

    def parse(self, phrase):
        result = False
        valid_trees = []
        lattice = create_word_lattice(phrase)
        earley_result, table  = earley_by_word_lattice(lattice, self.dm_cfg)
        if earley_result == False:
            return False, table, valid_trees
        for tree in table.get_trees(self.vocabulary.encoding):
            condition_nodes = [node for node in tree.descendants if node.condition != None]
            if all([check_condition(node, node.condition) for node in condition_nodes]):
                result = True
                valid_trees.append(tree)
        return result, table, valid_trees