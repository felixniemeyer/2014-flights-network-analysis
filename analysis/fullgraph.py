import networkx as nx
import sqlite3
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import collections

conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                       'Study/network-economics-case-study/db.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM routes WHERE airline_id=?", (5209,))
G = nx.DiGraph()
rows = cursor.fetchall()
for row in rows:
    if not G.has_edge(row[3], row[5]):
        G.add_edge(row[3], row[5])


# cursor.execute("SELECT * from airports")
# rows = cursor.fetchall()
# patronage = {}
# for row in rows:
#     patronage[row[0]] = row[15]

centrality = nx.degree_centrality(G)
print(centrality)
degreeCentr = []
for centr in centrality.values():
    degreeCentr.append(centr)
degree = []
frequency = []
counter = collections.Counter(degreeCentr)
for item in counter.keys():
    degree.append(item)
    frequency.append(counter[item])
plt.xscale('log')
plt.yscale('log')
plt.hist(degree, bins=np.linspace(0.0, 0.2, 200))
plt.show()




# pos = nx.spring_layout(G, scale=2)
# nx.draw_networkx(G, pos, with_labels=True, arrows=False, alpha=0.2, node_size=1, font_size=0.1, width=0.1)
# plt.savefig("unitedNetwork.png", bbox_inches='tight', format='png', dpi=300)
#

# def llllamda(key):
#     return patronage[key]
#
#
# plt.scatter(list(map(llllamda, (centrality.keys()))), centrality.values(), s=5)
# plt.xlabel("Patronage")
# plt.ylabel("Eigenvector Centrality")
# plt.savefig("Graph/patronage_eigenvector.png", bbox_inches='tight', format='png', dpi=300)
