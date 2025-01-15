"""
Georg Heindl 3493996
"""

import sys
import os

class GoldbergTarjan:
    def __init__(self, file):
        with open(file, 'r') as file:
            lines = file.readlines()
        self.n = int(lines[0].strip())
        self.edges = []
        for line in lines[1:]:
            u, v, capacity = map(int, line.strip().split())
            self.edges.append((u, v, capacity))

        self.adjacent = [[] for _ in range(self.n)]
        self.capacity = [[0] * self.n for _ in range(self.n)]
        self.height = [0] * self.n
        self.flow = [[0] * self.n for _ in range(self.n)]
        self.excess = [0] * self.n
       
        for u, v, cap in self.edges:
            self.capacity[u][v] = cap
            self.adjacent[u].append(v)
            self.adjacent[v].append(u)

        #Initialisierung, Quelle s = 0, Senke t = 1
        self.height[0] = self.n
        for v in self.adjacent[0]:
            self.flow[0][v] = self.capacity[0][v]
            self.flow[v][0] = -self.capacity[0][v]
            self.excess[v] = self.capacity[0][v]
            self.excess[0] -= self.capacity[0][v]

    def push(self, v, w):
        """
        Berechnet Gamma wie in der Vorlesung und augmentiert entlang der Kante (v, w).
        """
        gamma = min(self.excess[v], self.capacity[v][w] - self.flow[v][w])
        self.flow[v][w] += gamma
        self.flow[w][v] -= gamma
        self.excess[v] -= gamma
        self.excess[w] += gamma

    def relabel(self, v):
        """
        Berechnet Sigma(Height) wie in der Vorlesung.
        """
        min_height = float('inf')
        for w in self.adjacent[v]:
            if self.capacity[v][w] - self.flow[v][w] > 0:
                min_height = min(min_height, self.height[w])
        self.height[v] = min_height + 1

    def e_active_node(self):
        """
        Gibt einen aktiven Knoten zurück, falls vorhanden.
        """
        for v in range(self.n):
            if self.excess[v] > 0 and v != 0 and v != 1:
                return v
        return None

    def max_flow(self):
        """
        Berechnet den maximalen Fluss wie im Algorithmus aus Vorlesung.
        Erlaubte Kanten sind nur die, die Kapazität nicht ausgeschöpft und bei denen die Adjazenzknoten 1 tiefer liegen.
        """

        while True:                                                                                             #Zeile 3
            v = self.e_active_node()                                                                            #Zeile 3
            if v is None:                                                                                       #Zeile 3                       
                break                                                                                           #Zeile 3                                       
            pushed = False                                                                                      #Zeile 4                                      
            for w in self.adjacent[v]:                                                                          #Zeile 4                              
                if self.capacity[v][w] - self.flow[v][w] > 0 and self.height[v] == self.height[w] + 1:          #Zeile 4
                    self.push(v, w)                                                                             #Zeile 5    
                    pushed = True
                    break
            if not pushed:                                                                                      #Zeile 6      
                self.relabel(v)                                                                                 #Zeile 6
        return sum(self.flow[0][v] for v in self.adjacent[0])

    def __str__(self):
        """
        Produziert die Ausgabe wie in der Aufgabenstellung gefordert.
        """
        output = f"{self.max_flow()}\n"
        for idx, edge in enumerate(self.edges):
            v, w, _ = edge
            if self.flow[v][w] > 0:
                output += f"{idx} {self.flow[v][w]}\n"
        return output

def main():
    if len(sys.argv) != 2:
        print("Too many Arguments")
        sys.exit(1)
    file = sys.argv[1]
    if not os.path.isfile(file):
        print(f"{file} does not exist.")
        sys.exit(1)
    gt = GoldbergTarjan(file)
    print(gt)
    
if __name__ == "__main__":
    main()
