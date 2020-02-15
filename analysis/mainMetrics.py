import networkx as nx
import sqlite3
import analysis
import matplotlib.pyplot as plt
import scipy as sp

conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                       'Study/network-economics-case-study/db.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM Routes")
rows = cursor.fetchall()
print("Graph is going to be created")
G = nx.MultiDiGraph()
for row in rows:
    G.add_edge(row[3], row[5], weight=int(row[len(row) - 2]), flow=int(row[len(row) - 1]))
print("Graph has been created")

distDetails = []
distEdgeData = G.edges.data('weight')
sortedDistEdgeData = sorted(distEdgeData, key=lambda x: x[2], reverse=True)
listEdges = []
for edge in sortedDistEdgeData:
    listEdges.append(edge[2])
distDetails["dist_diameter"] = sortedDistEdgeData[0]
distDetails["totalDistance"] = G.size(weight='weight')
distDetails["avgDistance"] = G.size(weight='weight') / len(sortedDistEdgeData)

print(distDetails.items())

