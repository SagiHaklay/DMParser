import numpy as np
import pandas as pd
from anytree import AnyNode
from vocabulary import FeatureEncoding
from word_splitter import WordLattice

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
        self.nullables = {}
    def terminal_rules(self):
        return [rule for rule in self.rules if rule.is_terminal]
    
    def add_rule(self, left, right, is_terminal = False, cond = None):
        rule = CFGRule(left, right, is_terminal or (len(right) == 1 and right[0] in self.terminals), cond)
        self.rules.append(rule)
        if len(right) == 1 and (right[0] == "" or right[0] in self.nullables):
            self.nullables[left] = rule

    def get_terminals(self):
        return {rule.right[0] for rule in self.terminal_rules()}



            



class TableEntry:
    def __init__(self, rule: CFGRule, start_col, idx = 0, completing_entries = []) -> None:
        self.rule = rule
        self.completion_idx = idx
        self.start_col = start_col
        self.completing_entries = completing_entries

    def __repr__(self) -> str:
        return f'{self.rule.left} -> {" ".join(self.rule.right[:self.completion_idx])}.{" ".join(self.rule.right[self.completion_idx:])}[{self.start_col}]'

    def next_token(self):
        return self.rule.right[self.completion_idx]

    def incomplete(self):
        return self.completion_idx < len(self.rule.right)
    
    def get_completed_entry(self, completing_entry):
        return TableEntry(self.rule, self.start_col, self.completion_idx + 1, self.completing_entries + [completing_entry])
    
    def get_tree(self, decoder: FeatureEncoding | None = None):
        if len(self.completing_entries) == 0:
            features = decoder.decode(self.rule.left) if decoder is not None else self.rule.left
            return AnyNode(tag=features, condition=self.rule.condition)
        children = [entry.get_tree(decoder) for entry in self.completing_entries]
        return AnyNode(children=children, tag=self.rule.left, condition=self.rule.condition)
    
    
    def is_prediction(self, token):
        return self.rule.left == token and self.completion_idx == 0


class Table:
    def __init__(self, t) -> None:
        self.length = t
        self.columns = [[] for i in range(t + 1)]

    def __repr__(self) -> str:
        max_row_length = max(map(len, self.columns))
        return repr(pd.DataFrame(np.array([[repr(col[i]) if i < len(col) else "-" for col in self.columns] for i in range(max_row_length)])))
        #return "\n".join([repr(col) for col in self.columns])

    def add_entries(self, col, entries):
        self.columns[col] += entries

    def predictor(self, col, entry: TableEntry, g: CFG):
        if any([e.is_prediction(entry.next_token()) for e in self.columns[col]]):
            return
        self.add_entries(col, [TableEntry(rule, col) for rule in g.rules if rule.left == entry.next_token() and len(rule.right[0]) > 0 and rule.is_terminal == False])
        if entry.next_token() in g.nullables:
            rule = g.nullables[entry.next_token()]
            null_entry = TableEntry(rule, col, 1)
            self.add_entries(col, [entry.get_completed_entry(null_entry)])
    
    def completer(self, col, complete_entry: TableEntry):
        to_complete = [entry for entry in self.columns[complete_entry.start_col] if entry.incomplete() and entry.next_token() == complete_entry.rule.left]
        self.add_entries(col, [entry.get_completed_entry(complete_entry) for entry in to_complete])

    def get_last_entry(self) -> TableEntry | None:
        if len(self.columns[self.length]) == 0:
            return None
        return self.columns[self.length][-1]
    
    def get_success_entries(self):
        return [entry for entry in self.columns[self.length] if entry.rule.left == START]
    
    def get_tree(self, deocder=None):
        last_entry = self.get_last_entry()
        if last_entry is None or last_entry.incomplete():
            return None
        return last_entry.completing_entries[0].get_tree(deocder)
    
    
    def get_trees(self, decoder=None):
        success_entries = self.get_success_entries()
        return [entry.completing_entries[0].get_tree(decoder) for entry in success_entries]




def earley(tokens, g: CFG):
    t = len(tokens)
    #table = [[] for i in range(t + 1)]
    table = Table(t)
    #table[0].append(TableEntry(CFGRule(START, g.start_var), 0))
    table.add_entries(0, [TableEntry(CFGRule(START, [g.start_var]), 0)])
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
    #last_entry = table.get_last_entry()
    success_entries = table.get_success_entries()
    return len(success_entries) > 0, table

def earley_by_word_lattice(lattice: WordLattice, g: CFG):
    t = lattice.vertex_num - 1
    table = Table(t)
    table.add_entries(0, [TableEntry(CFGRule(START, [g.start_var]), 0)])
    terminal_rules = g.terminal_rules()
    for i in range(t + 1):
        if i > 0:
            # add tokens from the in edges of vertex i with start column according to source
            in_edges = lattice.get_edges_by_target(i)
            for e in in_edges:
                curr_token_rules = [rule for rule in terminal_rules if rule.right[0] == e['token']]
                table.add_entries(i, [TableEntry(rule, e.source, 1) for rule in curr_token_rules])
        for entry in table.columns[i]:
            if entry.incomplete():
               table.predictor(i, entry, g)
            else:
               table.completer(i, entry)
    success_entries = table.get_success_entries()
    return len(success_entries) > 0, table