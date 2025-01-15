import sys

"""
Ich habe Algorithmische Mathematik 1 nicht gehört, deshalb weiß ich nicht, welche Strukturen in Python verwendet werden dürfen
"""

class Bruecken:
    def __init__(self, file):
        with open(file, "r") as f:
            self.vertices = int(f.readline().strip())
            self.edges = [[] for _ in range(self.vertices)]
            edge_num = 0
            for line in f:
                edge_num += 1
                v, w = map(int, line.strip().split())
                self.edges[v].append(w)
                self.edges[w].append(v)
            recursion_limit = self.vertices if edge_num <= self.vertices else edge_num
            sys.setrecursionlimit(recursion_limit)      #Recursion Limit is 1000 by default for Python
        self.bridges = []                               #B
        self.time = 0                                   #i
        self.visited = [False] * self.vertices          #R
        self.disc_time = [-1] * self.vertices           #p 
        self.low = [-1] * self.vertices                 #Lowpoint
        
    def compare(self, place, bridge):
        """
        Compares two tuples by values, where the first value is the significant one.
        Returns True if place is smaller than bridge. 
        """
        if place[0] < bridge[0]:
            return True
        elif place[0] == bridge[0]:
            if place[1] < bridge[1]:
                return True
            else: False
        else:
            False
    
    def sort(self, bridges):
        """
        Sorts bridges in ascending order
        """
        n = len(bridges)
        if n <= 1: return bridges
        for i in range(n):
            bridges[i].sort()
        for i in range(1,n):
            place = bridges[i]
            j = i-1
            while j >= 0 and self.compare(place, bridges[j]):
                bridges[j+1] = bridges[j]
                j -= 1
            bridges[j+1] = place
        return bridges

    def berechne_bruecken(self):
        
        for i in range(self.vertices):
            if not self.visited[i]:
                self.dfs_visit(i, None)
        print(len(self.bridges))
        sorted_bridges = self.sort(self.bridges)
        for bridge in sorted_bridges:
            print(f"{bridge[0]} {bridge[1]}")

    def dfs_visit(self, v, pred):
        """
        Executes a DFS-visit similar to the algorithm in lecture
        """
        self.visited[v] = True
        self.time += 1
        self.disc_time[v] = self.low[v] = self.time
        
        for w in self.edges[v]:
            if not self.visited[w]:
                self.dfs_visit(w, v)

                self.low[v] = min(self.low[v], self.low[w])

                if self.low[w] > self.disc_time[v]:
                    self.bridges.append([v, w])
                    
            elif w != pred:

                self.low[v] = min(self.low[v], self.disc_time[w])

if __name__ == "__main__":
   graph = Bruecken(sys.argv[1])
   graph.berechne_bruecken() 


