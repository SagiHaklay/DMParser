from vocabulary import Vocabulary
from earley import CFG, earley

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
        return earley(phrase, self.dm_cfg)