START = "START"

class CFGRule:
    def __init__(self, left, right, is_terminal = False) -> None:
        self.left = left
        self.right = right
        self.is_terminal = is_terminal

    
    

class CFG:
    def __init__(self, start_var, terminals) -> None:
        self.rules = []
        self.start_var = start_var
        self.terminals = terminals

    def terminal_rules(self):
        return [rule for rule in self.rules if rule.is_terminal]
    
    def add_rule(self, left, right):
        self.rules.append(CFGRule(left, right, len(right) == 1 and right[0] in self.terminals))
    

class TableEntry:
    def __init__(self, rule: CFGRule, start_col, idx = 0) -> None:
        self.rule = rule
        self.completion_idx = idx
        self.start_col = start_col

    def __repr__(self) -> str:
        return f'{self.rule.left} -> {"".join(self.rule.right[:self.completion_idx])}.{"".join(self.rule.right[self.completion_idx:])}[{self.start_col}]'

    def next_token(self):
        return self.rule.right[self.completion_idx]

    def incomplete(self):
        return self.completion_idx < len(self.rule.right)
    
    def predictor(self, col, g: CFG, table):
        table[col] += [TableEntry(rule, col) for rule in g.rules if not rule.is_terminal and rule.left == self.next_token()]

    def get_completed_entry(self):
        return TableEntry(self.rule, self.start_col, self.completion_idx + 1)

    def completer(self, col, table):
        to_complete = [entry for entry in table[self.start_col] if not entry.rule.is_terminal and entry.next_token() == self.rule.left]
        table[col] += [entry.get_completed_entry() for entry in to_complete]


def earley(tokens, g: CFG):
    t = len(tokens)
    table = [[] for i in range(t + 1)]
    table[0].append(TableEntry(CFGRule(START, g.start_var), 0))
    terminal_rules = g.terminal_rules()
    for i in range(t + 1):
        if i > 0:
            curr_token_rules = [rule for rule in terminal_rules if rule.right[0] == tokens[i-1]]
            for rule in curr_token_rules:
                table[i].append(TableEntry(rule, i-1, 1))
        for entry in table[i]:
            if entry.incomplete():
               entry.predictor(i, g, table)
            else:
               entry.completer(i, table)
    return table[t][-1].rule.left == START, table

