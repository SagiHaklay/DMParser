START = "START"

class CFGRule:
    def __init__(self, left, right, is_terminal = False, condition = None) -> None:
        self.left = left
        self.right = right
        self.is_terminal = is_terminal
        self.condition = condition

    
    

class CFG:
    def __init__(self, start_var, terminals) -> None:
        self.rules = []
        self.start_var = start_var
        self.terminals = terminals
        self.nullables = []

    def terminal_rules(self):
        return [rule for rule in self.rules if rule.is_terminal]
    
    def add_rule(self, left, right, is_terminal = False, cond = None):
        self.rules.append(CFGRule(left, right, is_terminal or (len(right) == 1 and right[0] in self.terminals), cond))
        if len(right) == 1 and (right[0] == "" or right[0] in self.nullables):
            self.nullables.append(left)

    def get_terminals(self):
        return {rule.right[0] for rule in self.terminal_rules()}
    

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
        table[col] += [TableEntry(rule, col) for rule in g.rules if self.incomplete() and rule.left == self.next_token()]
        if self.next_token() in g.nullables:
            table[col] += [self.get_completed_entry()]

    def get_completed_entry(self):
        return TableEntry(self.rule, self.start_col, self.completion_idx + 1)

    def completer(self, col, table):
        to_complete = [entry for entry in table[self.start_col] if entry.incomplete() and entry.next_token() == self.rule.left]
        table[col] += [entry.get_completed_entry() for entry in to_complete]


class Table:
    def __init__(self, t) -> None:
        self.length = t
        self.columns = [[] for i in range(t + 1)]

    def __repr__(self) -> str:
        return repr(self.columns)

    def add_entries(self, col, entries):
        self.columns[col] += entries

    def predictor(self, col, entry: TableEntry, g: CFG):
        self.add_entries(col, [TableEntry(rule, col) for rule in g.rules if entry.incomplete() and rule.left == entry.next_token() and len(rule.right[0]) > 0])
        if entry.next_token() in g.nullables:
            self.add_entries(col, [entry.get_completed_entry()])
    
    def completer(self, col, complete_entry: TableEntry):
        to_complete = [entry for entry in self.columns[complete_entry.start_col] if entry.incomplete() and entry.next_token() == complete_entry.rule.left]
        self.add_entries(col, [entry.get_completed_entry() for entry in to_complete])

    def get_last_entry(self):
        if len(self.columns[self.length]) == 0:
            return None
        return self.columns[self.length][-1]


def earley(tokens, g: CFG):
    t = len(tokens)
    #table = [[] for i in range(t + 1)]
    table = Table(t)
    #table[0].append(TableEntry(CFGRule(START, g.start_var), 0))
    table.add_entries(0, [TableEntry(CFGRule(START, g.start_var), 0)])
    terminal_rules = g.terminal_rules()
    for i in range(t + 1):
        if i > 0:
            curr_token_rules = [rule for rule in terminal_rules if rule.right[0] == tokens[i-1]]
            for rule in curr_token_rules:
                #table[i].append(TableEntry(rule, i-1, 1))
                table.add_entries(i, [TableEntry(rule, i-1, 1)])
        for entry in table.columns[i]:
            if entry.incomplete():
               #entry.predictor(i, g, table)
               table.predictor(i, entry, g)
            else:
               #entry.completer(i, table)
               table.completer(i, entry)
    last_entry = table.get_last_entry()
    if last_entry is None:
        return False, table
    return last_entry.rule.left == START, table

