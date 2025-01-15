# Datei: boruvka_algorithmus.py

from collections import defaultdict

def boruvka_algorithm(file_path):
    # Eingabe des Graphen einlesen
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Anzahl der Knoten und Kanten einlesen
    n = int(lines[0].strip())
    edges = []
    for line in lines[1:]:
        u, v, weight = map(int, line.strip().split())
        edges.append((weight, u, v))

    # Initialisiere den MST
    mst_edges = []
    mst_weight = 0

    # Union-Find-Datenstruktur initialisieren
    parent = list(range(n))
    rank = [0] * n

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    # T hat k ≥ 2 Zsh-Komponenten
    num_components = n

    while num_components > 1:
        # Finde die günstigsten Kanten für jede Komponente
        cheapest = [-1] * n

        for weight, u, v in edges:
            root_u = find(u)
            root_v = find(v)
            if root_u != root_v:
                if cheapest[root_u] == -1 or weight < cheapest[root_u][0]:
                    cheapest[root_u] = (weight, u, v)
                if cheapest[root_v] == -1 or weight < cheapest[root_v][0]:
                    cheapest[root_v] = (weight, u, v)
        # Füge die günstigsten Kanten zum MST hinzu
        for i in range(n):
            if cheapest[i] != -1:
                weight, u, v = cheapest[i]
                root_u = find(u)
                root_v = find(v)
                if root_u != root_v:
                    union(u, v)
                    mst_edges.append((u, v, weight))
                    mst_weight += weight
                    num_components -= 1

    # Ergebnis ausgeben
    print(mst_weight)
    mst_edges_sorted = sorted([(min(u, v), max(u, v)) for u, v, weight in mst_edges])
    for u, v in mst_edges_sorted:
        print(u, v)

# Beispielaufruf:
boruvka_algorithm('alle_instanzen/inst_00')
