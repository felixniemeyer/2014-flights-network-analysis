import networkx as nx
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def sortedAirlines():
    conn = sqlite3.connect(
        '/home/sai/Documents/WiSe 2019-2020/Network Economics/Case Study/network-economics-case-study/db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT distinct airline_id FROM routes")
    rows = cursor.fetchall()
    airline_ids = []

    for row in rows:
        airline_ids.append(row)
    new_airline_list = []

    for item in airline_ids:
        cursornew = conn.cursor()
        cursornew.execute("SELECT COUNT(*) FROM routes WHERE airline_id =?", item)
        no_of_routes = cursornew.fetchall()
        listItem = list(item)
        new_airline_list.append([listItem[0], no_of_routes[0][0]])

    return sorted(new_airline_list, key=lambda x: x[1], reverse=True)


def draw(G, pos, measures, measure_name):
    nodes = nx.draw_networkx_nodes(G, pos, node_size=250, cmap=plt.cm.plasma,
                                   node_color=measures.values(),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))

    # labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos)

    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.savefig('centrality.png')