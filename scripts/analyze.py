import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
import geopy.distance

routes = nx.MultiDiGraph()

conn = sqlite3.connect('../fghjij.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM routes limit 100")

rows = cursor.fetchall()


def get_dist(orig, dest):
    coord = []
    cursor.execute("SELECT * from airports WHERE iata=? OR iata=?", (dest, orig))
    airports = cursor.fetchall()
    for airport in airports:
        coord.append((airport[6], airport[7]))
    if len(airports) == 2:
        return geopy.distance.vincenty(coord[0], coord[1]).km
    else:
        return 100


for row in rows:
    if not routes.has_edge(row[2], row[4], key=row[1]):
        dist = get_dist(row[2], row[4])
        routes.add_edge(row[2], row[4], key=row[1], dist=dist)

# with open('../data/routes.dat') as f:
#     csv_reader = csv.reader(f)
#     for row in csv_reader:
#         routes.add_edge(row[3], row[5])

nx.draw_networkx(routes, with_labels=True, node_size=10, font_size=2, arrowsize=4)
plt.savefig("./sample3.pdf", bbox_inches='tight', format='pdf', dpi=1200)
