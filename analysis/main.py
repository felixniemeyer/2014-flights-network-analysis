import networkx as nx
import sqlite3
import analysis
import matplotlib.pyplot as plt

# get a list of sorted airline IDs based on their frequency in the routes table
sortedAirlines = analysis.sortedAirlines()
G = []
for i in range(0, 1):
    conn = sqlite3.connect('/home/sai/Documents/WiSe 2019-2020/Network Economics/Case '
                           'Study/network-economics-case-study/db.db')
    cursor = conn.cursor()
    airlineId = str(sortedAirlines[i][0])
    cursor.execute("SELECT * FROM routes WHERE airline_id=?", (airlineId,))
    rows = cursor.fetchall()
    subG = nx.DiGraph()
    for row in rows:
        routeAttrs = {"dist": row[len(row) - 1], "passengerFlow": row[len(row) - 2]}
        routeKey = str(row[1]) + "_" + str(row[len(row) - 3])
        if not subG.has_edge(row[3], row[5]):
            subG.add_edge(row[3], row[5], length=int(row[len(row) - 1]), attrs=routeAttrs)
    G.append(subG)

for subG in G:
    print(nx.number_of_edges(subG))
    nx.draw_networkx(subG, with_labels=True, node_size=10, font_size=2, arrowsize=4)
    degrees = [subG.degree(n) for n in subG.nodes()]
    print(degrees)
    print(nx.betweenness_centrality(subG).items())
    #plt.hist(degrees, bins=500)
    #plt.show()
