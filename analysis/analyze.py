import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


routes = nx.MultiDiGraph()

with open('../data/routes.dat') as f: 
    csv_reader = csv.reader(f)
    for row in csv_reader: 
        routes.add_edge(row[3], row[5]) 

nx.draw_networkx(routes)
plt.show()
