import networkx as nx
import sqlite3
import matplotlib.pyplot as plt

# local modules
from network_loaders import loadAirlineNetwork
import largeness

G_lufthansa = loadAirlineNetwork('3320')
G_airfrance = loadAirlineNetwork('137')

l_lufthansa = largeness.calculateForGraph(G_lufthansa)
print('lufthansa largeness', l_lufthansa)
l_airfrance = largeness.calculateForGraph(G_airfrance)
print('airfrance largeness', l_airfrance)

G_both = nx.compose(G_lufthansa, G_airfrance)
l_both = largeness.calculateForGraph(G_both)
print('joint largeness', l_both)

print('cooperation opportunity', (l_lufthansa + l_airfrance ) /  l_both)

# nx.draw(G) 
# plt.show()
