from earley import earley, CFG, CFGRule

g = CFG("S", ["John", "speaks", "English"])
g.add_rule("S", ["NP", "VP"])
g.add_rule("NP", ["John"])
g.add_rule("NP", ["English"])
g.add_rule("VP", ["V", "NP"])
g.add_rule("V", ["speaks"])
result, table = earley(["John", "speaks", "English"], g)
print("result:", result)
print(table)