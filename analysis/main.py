import networkx as nx
import sqlite3
import analysis
import matplotlib.pyplot as plt
import scipy as sp

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
plt.hist(degreesList[0], bins=100, label=airlines[0], color=colors[0])
plt.hist(degreesList[1], bins=100, label=airlines[1], color=colors[1])
plt.hist(degreesList[2], bins=100, label=airlines[2], color=colors[2])
plt.xlabel("Degrees", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend()
plt.savefig('hist.png')
