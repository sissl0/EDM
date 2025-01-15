"""
Georg Heindl 3493996
"""

import sys
import os

class Boruvka():
    def __init__(self, file) -> None:
        """
        Layout for edges is [node1, node2, weight]
        Minimun spanning trees and its weight are saved seperat
        """
        with open(file, 'r') as f:
            lines = f.readlines()

        self.node_num = int(lines[0].strip())
        self.num_zsh = self.node_num
        self.g_edges = []
        self.g_rank = []
        self.predecessor = []
        for i in range(self.node_num):
            self.predecessor.append(i)
            self.g_rank.append(0)

        for line in lines[1:]:
            v, w, weight = map(int, line.strip().split())
            self.g_edges.append([v, w, weight])
        
        self.mst_edges = []
        self.mst_weight = 0

    def sort(self, edges):
        """
        Sorts edges ascending
        """
        _sorted = []
        for v,w,weight in edges:
            _sorted.append((min(v,w), max(v,w)))
        return sorted(_sorted)         

    def find_min_tree(self):
        """
        Merge until single Component
        """
        while self.num_zsh > 1:
            _min = [-1] * self.node_num
            """
            Find cheapest edges for every component
            """
            for v, w, weight in self.g_edges:
                pre_v = self.get_root(v)
                pre_w = self.get_root(w)
                if pre_v != pre_w:                                      #Edges of the same component can be ignored
                    if _min[pre_v] == -1 or _min[pre_v][2] > weight:
                        _min[pre_v] = [v,w,weight]
                    if _min[pre_w] == -1 or _min[pre_w][2] > weight:
                        _min[pre_w] = [v,w,weight]
            
            """
            Update new cheapest edges and merge Components accordingly
            """
            for n in range(self.node_num):
                if _min[n] != -1:
                    v, w, weight = _min[n]
                    pre_v = self.get_root(v)
                    pre_w = self.get_root(w)
                    if pre_v != pre_w:
                        self.mst_weight += weight
                        self.merge_by_rank(v,w)
                        self.num_zsh -= 1
                        self.mst_edges.append([v,w,weight])

    def get_root(self, node):
        """
        Recursivly search root
        """
        if self.predecessor[node] == node:
            return node
        else:
            return self.get_root(self.predecessor[node])

    def merge_by_rank(self, x, y):
        """
        Merge smaller tree at the root of higher tree by rank
        """
        pre_x = self.get_root(x)
        pre_y = self.get_root(y)
        if pre_x != pre_y:
            if self.g_rank[pre_x] > self.g_rank[pre_y]:
                self.predecessor[pre_y] = pre_x
            elif self.g_rank[pre_x] < self.g_rank[pre_y]:
                self.predecessor[pre_x] = pre_y
            else:
                self.predecessor[pre_y] = pre_x
                self.g_rank[pre_x] += 1
    
    def __str__(self) -> str:
        _sorted = self.sort(self.mst_edges)
        output = str(self.mst_weight) + "\n"
        for v, w in _sorted:
            output += f"{str(v)} {str(w)}\n"
        return output

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Too many Arguments")
        sys.exit(1)
    file = sys.argv[1]
    if not os.path.isfile(file):
        print(f"{file} does not exist.")
        sys.exit(1)
    boruvka = Boruvka(sys.argv[1])
    boruvka.find_min_tree()
    print(boruvka)

            