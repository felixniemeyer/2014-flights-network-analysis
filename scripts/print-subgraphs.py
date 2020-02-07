import networkx as nx

import network_loaders 

G = network_loaders.loadEntireNetwork()

G = nx.to_undirected(G)

connected_subgraphs = nx.connected_components(G)

for i, S in enumerate(connected_subgraphs): 
	print("Subgraph", i) 
	print("Number of nodes:", S)
	print(' '.join(list(S)))


