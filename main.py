from earley import CFG
from vocabulary import Vocabulary, FeatureEncoding
from parser import DMParser
from condition import Condition
from anytree import RenderTree
#import matplotlib.pyplot as plt
#import igraph as ig

features = ["v", "sagen", "1p", "2p", "3p", "singular", "plural", "past", "present"]
encoder = FeatureEncoding(features)
syntax = CFG("AgreeP", [])
#syntax.add_rule("S", ["nP", "T'"])
#syntax.add_rule("nP", ["n", "root"])
#syntax.add_rule("T'", ["AgreeP", "nP"])
syntax.add_rule("vP", ["v", "root"])
syntax.add_rule("AgreeP", ["tenseP", "AGR"])
syntax.add_rule("tenseP", ["vP", "tense"])
#syntax.add_rule("n", [encoder.encode({"n"})], True)
syntax.add_rule("v", [encoder.encode({"v"})], True)
syntax.add_rule("tense", [encoder.encode({"past"})], True)
syntax.add_rule("tense", [encoder.encode({"present"})], True)
syntax.add_rule("AGR", [encoder.encode({"1p", "singular"})], True)
syntax.add_rule("AGR", [encoder.encode({"2p", "singular"})], True)
syntax.add_rule("AGR", [encoder.encode({"3p", "singular"})], True)
syntax.add_rule("AGR", [encoder.encode({"1p", "plural"})], True)
syntax.add_rule("AGR", [encoder.encode({"2p", "plural"})], True)
syntax.add_rule("AGR", [encoder.encode({"3p", "plural"})], True)
#syntax.add_rule("root", [encoder.encode({"John"})], True)
#syntax.add_rule("root", [encoder.encode({"speak"})], True)
syntax.add_rule("root", [encoder.encode({"sagen"})], True)
vocabulary = Vocabulary(features)
#vocabulary.add_item({"John"}, [""], ["John"])
#vocabulary.add_item({"speak"}, [""], ["speak"])
vocabulary.add_item({"sagen"}, [None], ["sag"])
vocabulary.add_item({"past"}, [None], ["-te"])
vocabulary.add_item({"present"}, [None], [""])
vocabulary.add_item({"2p", "plural"}, [None], ["-t"])
vocabulary.add_item({"plural"}, [Condition("tense", [{"present"}], "AgreeP"), Condition("tense", [{"past"}], "AgreeP")], ["-en", "-n"])
vocabulary.add_item({"2p"}, [None], ["-st"])
vocabulary.add_item({"3p", "singular"}, [Condition("tense", [{"present"}], "AgreeP"), Condition("tense", [{"past"}], "AgreeP")], ["-t", ""])
#vocabulary.add_item({"n"}, [""], [""])
vocabulary.add_item({"v"}, [None], [""])
vocabulary.add_item(set(), [None], [""])
parser = DMParser(syntax, vocabulary)
result, table, valid_trees = parser.parse(["sag", "-te", "-n"])
print("result:", result)
print(table)

if result:
    #tree = table.get_tree(encoder)
    for tree in valid_trees:
        for pre, _, node in RenderTree(tree):
            print("%s%s" % (pre, node.tag))
