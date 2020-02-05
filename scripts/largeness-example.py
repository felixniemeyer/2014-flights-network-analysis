import networkx as nx
import sqlite3
import matplotlib.pyplot as plt
import sys

# local modules
from network_loaders import loadAirlineNetwork
import largeness

A_id = '3320'
B_id = '137'
if(len(sys.argv) == 3):
	A_id = sys.argv[1] 
	B_id = sys.argv[2]

G_A = loadAirlineNetwork(A_id)
G_B = loadAirlineNetwork(B_id)

l_A = largeness.calculateForGraph(G_A)
print('A largeness', l_A)
l_B = largeness.calculateForGraph(G_B)
print('B largeness', l_B)

G_both = nx.compose(G_A, G_B)
l_both = largeness.calculateForGraph(G_both)
print('joint largeness', l_both)

print('cooperation opportunity', l_both / (l_A + l_B ))

# nx.draw(G) 
# plt.show()
