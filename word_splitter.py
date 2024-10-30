from igraph import Graph

edges = [[0, 1], [1, 2], [1, 3], [1, 3], [1, 3], [2, 3], [2, 3], [2, 3]]
tokens = ['sag', 'te', 't', 'st', 'en', 't', 'st', 'n']
accept = [False, True, True, True]

class WordSplitter:
    def __init__(self) -> None:
        self.word_lattice = Graph(n=4, edges=edges, directed=True,
                                  edge_attrs={'token': tokens},
                                  vertex_attrs={'accept': accept})
        
    def split_word(self, word: str):
        v = self.word_lattice.vs[0]
        idx = 0
        active_queue = [(v, idx, [])]
        valid_splits = []
        while len(active_queue) > 0:
            v, idx, split = active_queue[0]
            active_queue = active_queue[1:]
            if idx >= len(word) and v['accept']:
                valid_splits.append(split)
            for e in v.out_edges():
                token = e['token']
                if word.startswith(token, idx):
                    target = self.word_lattice.vs[e.target]
                    next_idx = idx + len(token)
                    active_queue.append((target, next_idx, split + [token]))
        return valid_splits
    
splitter = WordSplitter()
print(splitter.split_word('sagten'))