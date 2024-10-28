from earley import CFG
from vocabulary import Vocabulary, FeatureEncoding
from parser import DMParser
from anytree import RenderTree
#import matplotlib.pyplot as plt
#import igraph as ig

features = ["v", "sagen", "1p", "2p", "3p", "singular", "plural", "past"]
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
vocabulary.add_item({"sagen"}, [""], ["sag"])
vocabulary.add_item({"past"}, [""], ["-te"])
vocabulary.add_item({"2p", "plural"}, [""], ["-t"])
vocabulary.add_item({"plural"}, [""], ["-n"])
vocabulary.add_item({"2p"}, [""], ["-st"])
#vocabulary.add_item({"n"}, [""], [""])
vocabulary.add_item({"v"}, [""], [""])
vocabulary.add_item(set(), [""], [""])
parser = DMParser(syntax, vocabulary)
result, table = parser.parse(["sag", "-te", "-st"])
print("result:", result)
print(table)

if result:
    tree = table.get_tree(encoder)
    for pre, _, node in RenderTree(tree):
        print("%s%s" % (pre, node.tag))
