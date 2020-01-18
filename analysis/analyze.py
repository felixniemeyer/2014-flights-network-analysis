import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sqlite3


routes = nx.MultiDiGraph()

conn = sqlite3.connect('../fghjij.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM routes WHERE airline_id='4066'")

rows = cursor.fetchall()
for row in rows:
    routes.add_edge(row[3], row[5])

# with open('../data/routes.dat') as f:
#     csv_reader = csv.reader(f)
#     for row in csv_reader:
#         routes.add_edge(row[3], row[5])

nx.draw_networkx(routes)
plt.show()
