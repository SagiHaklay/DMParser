class VocabularyItem:
    def __init__(self, feature_set, conditions, values) -> None:
        self.feature_set = feature_set
        self.conditions = conditions
        self.values = values


class FeatureEncoding:
    def __init__(self, features) -> None:
        self.all_features = features

    def encode(self, features_to_encode):
        return "".join(['1' if feature in features_to_encode else '0' for feature in self.all_features])
    
    def decode(self, encoded_features):
        return {feature for feature, in_set in zip(self.all_features, encoded_features) if in_set == '1'}
    
class Vocabulary:
    def __init__(self, all_features) -> None:
        self.encoding = FeatureEncoding(all_features)
        self.vocabulary_items = {}

    def add_item(self, feature_set, conditions, values):
        key = self.encoding.encode(feature_set)
        self.vocabulary_items[key] = VocabularyItem(feature_set, conditions, values)

    def get_item(self, feature: set | str) -> VocabularyItem | None:
        if isinstance(feature, set):
            key = self.encoding.encode(feature)
            feature_set = feature
        else:
            key = feature
            feature_set = self.encoding.decode(feature)
        if key in self.vocabulary_items:
            return self.vocabulary_items[key]
        else:
            subsets = [v.feature_set for k, v in self.vocabulary_items.items() if v.feature_set <= feature_set]
            if len(subsets) == 0:
                return None
            sorted_subsets = sorted(subsets, key=lambda s: len(s), reverse=True)
            key = self.encoding.encode(sorted_subsets[0])
            return self.vocabulary_items[key]
        
    def phonological_values(self):
        result = set()
        for k in self.vocabulary_items:
            result = result.union(self.vocabulary_items[k].values)
        return result


        