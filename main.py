from earley import earley, CFG, CFGRule

g = CFG("S")
g.rules.append(CFGRule("S", ["NP", "VP"]))
g.rules.append(CFGRule("NP", ["John"], True))
g.rules.append(CFGRule("NP", ["English"], True))
g.rules.append(CFGRule("VP", ["V", "NP"]))
g.rules.append(CFGRule("V", ["speaks"], True))
result, table = earley(["John", "speaks", "English"], g)
print("result:", result)
print(table)