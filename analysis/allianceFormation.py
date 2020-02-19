import operator

import networkx as nx
import sqlite3
import numpy as np


def common(a, b):
    c = [value for value in a if value in b]
    return c


def allianceForms(subG1, nodes1, centrality1, path2MatrixSum1, path3MatrixSum1, airlineId):
    if len(airlineId) > 3:
        signiFactor = {}
        for i in range(0, len(airlineId)):
            for j in range(i + 1, len(airlineId)):
                x = 0
                commonNodes = common(nodes1[airlineId[i]], nodes1[airlineId[j]])
                for eachNode in commonNodes:
                    x += centrality1[airlineId[i]][eachNode] * centrality1[airlineId[j]][eachNode]

                combinedG = nx.DiGraph()
                combinedG = nx.compose(subG1[airlineId[i]], subG1[airlineId[j]])
                adjMat = nx.adjacency_matrix(combinedG).todense()
                path2combinedG = np.matmul(adjMat, adjMat)
                path3combinedG = np.matmul(path2combinedG, adjMat)
                path2combinedSum = path2combinedG.sum()
                path3combinedSum = path3combinedG.sum()
                y = 0
                y = path2combinedSum / (path2MatrixSum1[airlineId[i]] + path2MatrixSum1[airlineId[j]])
                z = path3combinedSum / (path3MatrixSum1[airlineId[i]] + path3MatrixSum1[airlineId[j]])
                signiFactor[i, j] = x * y + x * z

        sorted_Alliances = sorted(signiFactor.items(), key=operator.itemgetter(1), reverse=True)
        id1 = airlineId[sorted_Alliances[0][0][0]]
        id2 = airlineId[sorted_Alliances[0][0][1]]
        print(airlineId)
        print(sorted_Alliances[0][0][0])
        print(sorted_Alliances[0][0][1])
        airlineId.pop(sorted_Alliances[0][0][0])
        airlineId.pop(sorted_Alliances[0][0][1] - 1)
        print(airlineId)
        print("Alliance: ", id1)
        print("And: ", id2)
        print(str(id1) + str(id2))
        newAllianceGraph = nx.compose(subG1[id1], subG1[id2])

        subG1.pop(id1)
        subG1.pop(id2)
        subG1[str(id1) + str(id2)] = newAllianceGraph

        nodes1.pop(id1)
        nodes1.pop(id2)
        nodes1[str(id1) + str(id2)] = newAllianceGraph.nodes()

        centrality1.pop(id1)
        centrality1.pop(id2)
        centrality1[str(id1) + str(id2)] = nx.eigenvector_centrality(newAllianceGraph)
        path2MatrixSum1.pop(id1)
        path2MatrixSum1.pop(id2)
        path3MatrixSum1.pop(id1)
        path3MatrixSum1.pop(id2)

        adjMat = nx.adjacency_matrix(newAllianceGraph).todense()
        path2Mat = np.matmul(adjMat, adjMat)
        path3Mat = np.matmul(path2Mat, adjMat)
        path2MatrixSum1[str(id1) + str(id2)] = path2Mat.sum()
        path3MatrixSum1[str(id1) + str(id2)] = path3Mat.sum()
        airlineId.append(str(id1) + str(id2))

        print("airline IDs are :", airlineId)
        allianceForms(subG1, nodes1, centrality1, path2MatrixSum1, path3MatrixSum1, airlineId)

    else:
        return 0


airlineIds = [1191, 1057, 319, 1066, 2857, 2104]
airlineName = ['Air Austral', 'Air Mauritius', 'Air Seychelles', 'Air Madagascar', 'Indonesia Air Asia',
               'East African Safari']

conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                       'Study/network-economics-case-study/db.db')

cursor = conn.cursor()
subG = {}
nodes = {}
centrality = {}
adjMatrixSum = {}
path2MatrixSum = {}
path3MatrixSum = {}

for i in range(0, 6):
    cursor.execute("SELECT * FROM routes WHERE airline_id=?", (airlineIds[i],))
    subG[airlineIds[i]] = nx.DiGraph()
    rows = cursor.fetchall()
    for row in rows:
        subG[airlineIds[i]].add_edge(row[3], row[5], airline=airlineIds[i])

    # list of nodes in each graph
    nodes[airlineIds[i]] = subG[airlineIds[i]].nodes()
    print(nodes[airlineIds[i]])
    # calculating centrality for this graph
    centrality[airlineIds[i]] = nx.eigenvector_centrality(subG[airlineIds[i]])

    # to calculate adj, path2 path3 for this graph
    adjM = nx.adjacency_matrix(subG[airlineIds[i]]).todense()
    path2M = np.matmul(adjM, adjM)
    path3M = np.matmul(path2M, adjM)
    adjMatrixSum[airlineIds[i]] = adjM.sum()
    path2MatrixSum[airlineIds[i]] = path2M.sum()
    path3MatrixSum[airlineIds[i]] = path3M.sum()
    i += 1

allianceForms(subG, nodes, centrality, path2MatrixSum, path3MatrixSum, airlineIds)
