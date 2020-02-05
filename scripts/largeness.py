import networkx as nx
import numpy as np
import math



def calculateForGraph(G): 
	nodes = list(G.nodes())
	adjm = nx.to_numpy_matrix(G, dtype=int, multigraph_weight='min')	

	square = np.linalg.matrix_power(adjm, 2) 
	
	(n, m) = np.shape(square) 
	largeness = 0
	for i in range(n): 
		for j in range(m): 
			if square[i,j] > 0: #and adjm[i,j] = 0 just an idea
				sa_node = G.nodes[nodes[i]]
				da_node = G.nodes[nodes[j]]
				largeness += math.sqrt(sa_node["patronage"] * da_node["patronage"])

	return largeness
