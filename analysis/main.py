import networkx as nx
import sqlite3
import analysis
import matplotlib.pyplot as plt
import scipy as sp


# get a list of sorted airline IDs based on their frequency in the routes table
sortedAirlines = analysis.sortedAirlines()
G = []
for i in range(0, 1):
    conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                           'Study/network-economics-case-study/db.db')
    cursor = conn.cursor()
    airlineId = str(sortedAirlines[i][0])
    print(airlineId)
    cursor.execute("SELECT * FROM routes WHERE airline_id=?", (airlineId,))
    rows = cursor.fetchall()
    subG = nx.DiGraph()
    for row in rows:
        if not subG.has_edge(row[3], row[5]):
            subG.add_edge(row[3], row[5], weight=int(row[len(row) - 2]), flow=int(row[len(row) - 1]))
    G.append(subG)

for subG in G:
    print(subG.size())
    print(subG.size(weight='weight'))
    print(subG.size(weight='flow'))
    adjacencyMatrix = nx.adjacency_matrix(subG)
    #print(adjacencyMatrix)
    distEdgeData = subG.edges.data('weight')
    sortedDistEdgeData = sorted(distEdgeData, key=lambda x: x[2], reverse=True)
    print("dist diameter: ", sortedDistEdgeData[0])
    flowEdgeData = subG.edges.data('flow')
    sortedFlowEdgeData = sorted(flowEdgeData, key=lambda x: x[2], reverse=True)
    print("flow diameter: ", sortedFlowEdgeData[0])
    edgeData = subG.edges.data()
    listEdgeData = []
    for edges in edgeData:
        listEdgeData.append([edges[0], edges[1], edges[2]['weight']*edges[2]['flow']])
    sortedEdgeData = sorted(listEdgeData, key=lambda x: x[2], reverse=True)
    print("net diameter: ", sortedEdgeData[0])
    print(nx.average_shortest_path_length(subG))
    dictCentrality = nx.closeness_centrality(subG)
    listCentrality = []
    for key in dictCentrality:
        listCentrality.append([key, dictCentrality[key]])
    sortedCentrality = sorted(listCentrality, key=lambda x: x[1], reverse=True)
    print("most prestigious node: ", sortedCentrality[0])

    #nx.draw_networkx(subG, with_labels=True, node_size=10, font_size=2, arrowsize=4)
    degrees = [subG.degree(n) for n in subG.nodes()]
    print(degrees)
    print(nx.algorithms.distance_measures.diameter(subG, ))
    #plt.hist(degrees, bins=50)
    #plt.show()
