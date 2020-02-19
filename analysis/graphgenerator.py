import networkx as nx
import sqlite3
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import collections

conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                       'Study/network-economics-case-study/db.db')

cursor = conn.cursor()
airlineId = [5209, 3320, 4296, 4547]
color = ['red', 'blue', 'magenta', 'green']
airlines = ['United', 'Lufthansa', 'Ryan', 'Southwest']
subG = []
G = nx.DiGraph()

for i in range(0, 4):
    cursor.execute("SELECT * FROM routes WHERE airline_id=?", (airlineId[i],))
    subG.append(nx.DiGraph())
    rows = cursor.fetchall()
    for row in rows:
        subG[i].add_edge(row[3], row[5], airline=airlineId[i], weight=int(row[len(row) - 2]))
    i += 1

for i in range(0, 4):
    eigen_centrality = nx.eigenvector_centrality(subG[i])
    eigen_ctr = []
    for value in eigen_centrality.values():
        eigen_ctr.append(value)
    print(eigen_ctr)
    density = stats.gaussian_kde(eigen_ctr)
    bins = np.linspace(-0.5, 1, 500)
    plt.plot(bins, density(bins), color=color[i], label=airlines[i])

plt.xlabel("Eigenvector Centrality", fontsize=12)
plt.ylabel("Occurences in %", fontsize=12)
plt.legend()
plt.savefig("Graph/eigenvector_hist.png", bbox_inches='tight', format='png', dpi=300)







"""
for i in range(0, 4):
    closeness_centrality = nx.closeness_centrality(subG[i])
    cls_ctr = []
    for value in closeness_centrality.values():
        cls_ctr.append(value)
    density = stats.gaussian_kde(cls_ctr)
    bins = np.linspace(0, 1, 500)
    plt.plot(bins, density(bins), color=color[i], label=airlines[i])

plt.xlabel("Closeness Centrality", fontsize=12)
plt.ylabel("Occurences in %", fontsize=12)
plt.legend()
plt.savefig("Graph/closeness_hist.png", bbox_inches='tight', format='png', dpi=300)
"""

"""
for i in range(0, 4):
    dist = []
    distances = subG[i].edges.data('weight')
    for each in distances:
        dist.append(each[2])
    density = stats.gaussian_kde(dist)
    # n, x, _ = plt.hist(dist, bins=np.linspace(0, 15000, 200), histtype='step', density=True, color=color[i])
    bins = np.linspace(0, 15000, 200)
    plt.plot(bins, density(bins) * 100, color=color[i], label=airlines[i])

plt.xlabel("Distance (km)", fontsize=12)
plt.ylabel("Occurences in %", fontsize=12)
plt.legend()
plt.savefig("Graph/distance_hist.png", bbox_inches='tight', format='png', dpi=300)
"""

