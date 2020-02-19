import networkx as nx
import sqlite3
import analysis
import matplotlib.pyplot as plt
import scipy as sp
import statistics
import collections
import numpy as np
from matplotlib.lines import Line2D

airlineId = [1191, 1057, 319, 1066]
airlineName = ['Air Austral', 'Air Mauritius', 'Air Seychelles', 'Air Madagascar']

conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                       'Study/network-economics-case-study/db.db')

cursor = conn.cursor()
color = ['red', 'blue', 'magenta', 'green']
subG = []
G = nx.DiGraph()
midG1 = nx.DiGraph()
midG2 = nx.DiGraph()
print("Before forming alliance: ")
for i in range(0, 4):
    cursor.execute("SELECT * FROM routes WHERE airline_id=?", (airlineId[i],))
    subG.append(nx.DiGraph())
    rows = cursor.fetchall()
    for row in rows:
        subG[i].add_edge(row[3], row[5], airline=airlineId[i])
    adjM = nx.adjacency_matrix(subG[i]).todense()
    path2M = np.matmul(adjM, adjM)
    path3M = np.matmul(path2M, adjM)
    print("For the Airline: ", airlineName[i])
    subGraphSum1 = adjM.sum()
    subGraphSum2 = path2M.sum()
    subGraphSum3 = path3M.sum()
    print("Total Routes: ", subGraphSum1)
    print("Total Path 2 routes: ", subGraphSum2)
    print("Total Path 3 routes: ", subGraphSum3)
    i += 1

midG1 = nx.compose(subG[0], subG[1])
midG2 = nx.compose(midG1, subG[2])
G = nx.compose(midG2, subG[3])


def make_proxy(clrx, **kwargs):
    return Line2D([0, 0.5], [0, 0.5], color=clrx, **kwargs)


# generate proxies with the above function
proxies = [make_proxy(clr, lw=5) for clr in color]

pos = nx.spring_layout(G, scale=2)
for i in range(0, 4):
    nx.draw_networkx(G, pos, edgelist=subG[i].edges(), alpha=0.8, node_size=100, font_size=5,
                     edge_color=color[i], arrowsize=5)

# user airlineName as label for legend
plt.legend(proxies, airlineName, prop={"size": 5})
plt.savefig("vanillaAlliance.png", bbox_inches='tight', format='png', dpi=1200)

adjMatrix = nx.adjacency_matrix(G).todense()
path2Matrix = np.matmul(adjMatrix, adjMatrix)
path3Matrix = np.matmul(path2Matrix, adjMatrix)

sum1 = adjMatrix.sum()
sum2 = path2Matrix.sum()
sum3 = path3Matrix.sum()
print("After forming Alliance:")
print("Total Routes: ", sum1)
print("Total Path 2 routes: ", sum2)
print("Total Path 3 routes: ", sum3)

textFile = open("adjMatrix.txt", "w")
textFile.write(str(adjMatrix))


pos = nx.spring_layout(subG, scale=2)
nx.draw_networkx(subG, pos, with_labels=True, arrows=False, alpha=0.2, node_size=1, font_size=0.1, width=0.1)
plt.savefig("southWest.png", bbox_inches='tight', format='png', dpi=300)



# edgeLengths = subG.edges.data('flow')
# sortedEdgeLengths = sorted(edgeLengths, key=lambda x: x[2], reverse=True)
# descEdgeLengths = [x[2] for x in sortedEdgeLengths]
# print("diameter: ", descEdgeLengths[0])
# print("mean: ", statistics.mean(descEdgeLengths))
# print("median: ", statistics.median(descEdgeLengths))

# centrality = nx.eigenvector_centrality(subG).values()
# listCentrality = []
# for i in centrality:
#     listCentrality.append(i)
#
# print(listCentrality)
#
# counter = collections.Counter(listCentrality)
# plt.scatter(counter.keys(), counter.values(), s=np.pi, alpha=0.5, c='red', label='United Airlines')
# plt.xlabel("Eigenvalue Centrality")
# plt.ylabel("No. of Nodes")
# plt.xlim([0, 0.45])
# plt.ylim([0, 60])
# plt.legend()
# plt.savefig("unitedEigenValueCentrality.png", bbox_inches='tight', format='png', dpi=1200)





"""
# get a list of sorted airline IDs based on their frequency in the routes table
sortedAirlines = analysis.sortedAirlines()
airlines = []
G = []
for i in range(0, 7):
    conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                           'Study/network-economics-case-study/db.db')
    cursor = conn.cursor()
    airlineId = str(sortedAirlines[i][0])
    cursor.execute("SELECT name FROM airlines where airline_id=?", (airlineId,))
    airlines.append(cursor.fetchone())
    cursor.execute("SELECT * FROM routes WHERE airline_id=?", (airlineId,))
    rows = cursor.fetchall()
    subG = nx.DiGraph()
    for row in rows:
        if not subG.has_edge(row[3], row[5]):
            subG.add_edge(row[3], row[5], weight=int(row[len(row) - 2]), flow=int(row[len(row) - 1]))
    G.append(subG)

colors = ["g", "b", "r"]
distGraph = []
flowGraph = []
centralityGraph = []
details = []
degreesList = []
i = 0
for subG in G:
    dictDetails = {}
    dictDetails["name"] = airlines[i]
    # adjacencyMatrix = nx.adjacency_matrix(subG)
    # print(adjacencyMatrix)
    distEdgeData = subG.edges.data('weight')
    sortedDistEdgeData = sorted(distEdgeData, key=lambda x: x[2], reverse=True)
    listEdges = []
    for edge in sortedDistEdgeData:
        listEdges.append(edge[2])
    distGraph.append(listEdges)
    dictDetails["dist_diameter"] = sortedDistEdgeData[0]
    dictDetails["totalDistance"] = subG.size(weight='weight')
    dictDetails["avgDistance"] = subG.size(weight='weight') / len(sortedDistEdgeData)
    flowEdgeData = subG.edges.data('flow')
    sortedFlowEdgeData = sorted(flowEdgeData, key=lambda x: x[2], reverse=True)
    flowListEdgeData = []
    for edge in sortedFlowEdgeData:
        flowListEdgeData.append(edge[2])
    flowGraph.append(flowListEdgeData)
    dictDetails["flow_diameter"] = sortedFlowEdgeData[0]
    dictDetails["totalFlow"] = subG.size(weight='flow')
    dictDetails["avgFlow"] = subG.size(weight='flow') / len(flowListEdgeData)
    edgeData = subG.edges.data()
    listEdgeData = []
    for edges in edgeData:
        listEdgeData.append([edges[0], edges[1], edges[2]['weight'] * edges[2]['flow']])
    sortedEdgeData = sorted(listEdgeData, key=lambda x: x[2], reverse=True)
    dictDetails["net_diameter"] = sortedEdgeData[0]
    dictDetails["avg_clustering_dist"] = nx.average_clustering(subG, weight='weight')
    dictDetails["avg_clustering_flow"] = nx.average_clustering(subG, weight='flow')
    #print(nx.average_shortest_path_length(subG))
    details.append(dictDetails)
    dictCentrality = nx.eigenvector_centrality(subG)
    listCentrality = []
    for key in dictCentrality:
        listCentrality.append([key, dictCentrality[key]])
    sortedCentrality = sorted(listCentrality, key=lambda x: x[1], reverse=True)
    sortedListCentrality = []
    for centrality in sortedCentrality:
        sortedListCentrality.append(centrality[1])
    centralityGraph.append(sortedListCentrality)

    # nx.draw_networkx(subG, with_labels=True, node_size=10, font_size=2, arrowsize=4)
    degrees = [subG.degree(n) for n in subG.nodes()]
    degreesList.append(degrees)
    i += 1
    # plt.hist(degrees, bins=50)
    # plt.show()
with open('stats.txt', 'w') as f:
    print(details, file=f)


pos = nx.spring_layout(G[0])


#analysis.draw(G[0], pos, nx.degree_centrality(G), 'Degree Centrality')
plt.hist(degreesList[0], bins=100, label=airlines[0], color=colors[0], histtype='step')
plt.hist(degreesList[1], bins=100, label=airlines[1], color=colors[1], histtype='step')
plt.hist(degreesList[2], bins=100, label=airlines[2], color=colors[2], histtype='step')
plt.xlabel("Degrees", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend()
plt.savefig('hist.png', dpi=600)
"""
