from igraph import Graph, plot
import matplotlib.pyplot as plt

class WordLattice:
    def __init__(self) -> None:
        self.edges = []
        self.edge_tokens = []
        self.vertex_num = 0

    def add_edge(self, source, target, token):
        self.edges.append((source, target))
        self.edge_tokens.append(token)
        self.vertex_num = max([source+1, target+1, self.vertex_num])

    def to_graph(self):
        return Graph(n=self.vertex_num, edges=self.edges, directed=True,
                  edge_attrs={'token': self.edge_tokens})

    def get_edges_by_target(self, target):
        g = self.to_graph()
        return g.vs[target].in_edges()
    
    def show(self):
        g = self.to_graph()
        fig, ax = plt.subplots(figsize=(5, 5))
        plot(g, target=ax, layout="circle", edge_label=g.es['token'])
        plt.show()

class WordSplitter:
    def __init__(self, lattice) -> None:
        self.word_lattice = lattice
        
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
    
def create_word_lattice(phrase: str):
    word_list = phrase.split()
    lattice = WordLattice()
    start = 0
    for word in word_list:
        word_len = len(word)
        for i in range(word_len):
            for j in range(i+1, word_len+1):
                lattice.add_edge(start + i, start + j, word[i:j])
        start += word_len
    return lattice
    