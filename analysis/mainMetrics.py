import collections
import networkx as nx
import sqlite3
import analysis
import matplotlib.pyplot as plt
import scipy
from scipy import stats
import numpy as np

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

distDetails = {}
distEdgeData = G.edges.data('weight')
sortedDistEdgeData = sorted(distEdgeData, key=lambda x: x[2], reverse=True)
listEdges = []
for edge in sortedDistEdgeData:
    listEdges.append(edge[2])
distDetails["dist_diameter"] = sortedDistEdgeData[0]
distDetails["totalDistance"] = G.size(weight='weight')
distDetails["avgDistance"] = G.size(weight='weight') / len(sortedDistEdgeData)

print(distDetails.items())

dictDegCentr = nx.degree_centrality(G)
listDegCentr = []
for key in dictDegCentr:
    listDegCentr.append([key, dictDegCentr[key]])
sortedDegCentr = sorted(listDegCentr, key=lambda x: x[1], reverse=True)
sortedListDegCentr = []
for centrality in sortedDegCentr:
    sortedListDegCentr.append(centrality[1])

# plt.hist(sortedListDegCentr, bins=750, range=[0, 0.2])
# plt.xlabel("Degree Centrality", fontsize=12)
# plt.ylabel("Frequency", fontsize=12)
# plt.savefig('hist.png', dpi=600)

counterListDegCentr = collections.Counter(sortedListDegCentr)

print(counterListDegCentr)
sortedListDegCentr = list(counterListDegCentr.keys())
sortedListDegCentrCount = list(counterListDegCentr.values())

max_degree = max(sortedListDegCentrCount)


def f(x1, c1, a1):
    return c1 * np.power(x1, -a1)


def f_log(x2, c2, a2):
    return np.log(f(np.exp(x2), c2, a2))


mc = 4900
ma = 1.55

# least square fit
((c, a), pcov) = scipy.optimize.curve_fit(f, sortedListDegCentr, sortedListDegCentrCount, p0=(100, 0.5))

# least square fit on log
log_degrees = np.log(sortedListDegCentr)
((lc, la), pcov) = scipy.optimize.curve_fit(f_log, np.log(sortedListDegCentr), np.log(sortedListDegCentrCount), p0=(mc, ma))

x = np.logspace(1, np.log10(max_degree), 100)

# plt.plot(x, f(x, c, a), color='red')
# plt.plot(x, f(x, lc, la), color='green')
# plt.plot(x, f(x, mc, ma), color='orange')

plt.scatter(sortedListDegCentr, sortedListDegCentrCount, marker=0)

plt.xlabel('degree centrality')
plt.ylabel('number of nodes')

plt.xscale('log')
plt.yscale('log')

labels = [
    'curve_fit: ${0:.2f}*e^{{-{1:.2f}d}}$'.format(c, a),
    'curve_fit, log(y): ${0:.2f}*e^{{-{1:.2f}d}}$'.format(lc, la),
    'manual: ${0:.2f}*e^{{-{1:.2f}d}}$'.format(mc, ma),
    'nodes per degree',
]
plt.legend(labels, loc=1)

plt.savefig('degree_centrality_curve_manual.png', dpi=600, bbox_inches='tight')

# x_d = np.linspace(0, 0.2, len(sortedListDegCentr))
# density = sum(stats.norm(x_d).pdf(xi) for xi in sortedListDegCentr)
# plt.fill_between(x_d, density, alpha=0.5)
# plt.plot(sortedListDegCentr, np.full_like(sortedListDegCentr, -0.1), '|k', markeredgewidth=1)
# plt.savefig('kernel.png')
