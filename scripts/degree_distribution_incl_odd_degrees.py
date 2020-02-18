import collections
import matplotlib.pyplot as plt 
import numpy as np
import math
import scipy.optimize

import network_loader 

network = network_loader.load()

degree_counts = {}
max_degree = 0

for n, d in network.degree():
	try:
		degree_counts[d] += 1
	except:
		degree_counts[d] = 1
	if d > max_degree: 
		max_degree = d

degrees = []
nodes = []

for degree_count in degree_counts:
	degrees.append(degree_count)
	nodes.append(degree_counts[degree_count])
	
degrees = np.array(degrees)
nodes = np.array(nodes) 

 
plt.scatter(degrees, nodes, marker='o', s=10)

plt.xlabel('degree')
plt.ylabel('number of nodes')

plt.xscale('log')
plt.yscale('log')

plt.savefig('./results/degree_distribution_incl_odd_degrees.png', dpi=300, bbox_inches='tight')
plt.show()

