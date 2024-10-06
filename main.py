from earley import CFG
from vocabulary import Vocabulary, FeatureEncoding
from parser import DMParser

features = {"n", "v", "John", "speak", "English", "1p", "2p", "3p", "singular", "plural", "present"}
encoder = FeatureEncoding(features)
syntax = CFG("S", [])
syntax.add_rule("S", ["nP", "T'"])
syntax.add_rule("nP", ["n", "root"])
syntax.add_rule("T'", ["AgreeP", "nP"])
syntax.add_rule("vP", ["v", "root"])
syntax.add_rule("AgreeP", ["tenseP", "AGR"])
syntax.add_rule("tenseP", ["vP", "tense"])
syntax.add_rule("n", [encoder.encode({"n"})], True)
syntax.add_rule("v", [encoder.encode({"v"})], True)
syntax.add_rule("tense", [encoder.encode({"present"})], True)
syntax.add_rule("AGR", [encoder.encode({"3p", "singular"})], True)
syntax.add_rule("root", [encoder.encode({"John"})], True)
syntax.add_rule("root", [encoder.encode({"speak"})], True)
syntax.add_rule("root", [encoder.encode({"English"})], True)
vocabulary = Vocabulary(features)
vocabulary.add_item({"John"}, [""], ["John"])
vocabulary.add_item({"speak"}, [""], ["speak"])
vocabulary.add_item({"English"}, [""], ["English"])
vocabulary.add_item({"present"}, ["_[3p, singular]", "elsewhere"], ["-s", ""])
vocabulary.add_item({"3p", "singular"}, [""], [""])
vocabulary.add_item({"n"}, [""], [""])
vocabulary.add_item({"v"}, [""], [""])
parser = DMParser(syntax, vocabulary)
result, table = parser.parse(["John", "speak", "-s", "English"])
print("result:", result)
print(table)