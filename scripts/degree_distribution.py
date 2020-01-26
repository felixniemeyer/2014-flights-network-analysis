import collections
import matplotlib.pyplot as plt 
import numpy as np

from network_loader import loadNetwork

routes = loadNetwork()

degree_count = {}
max_degree = 0

for n, d in routes.degree():
	try:
		degree_count[d] += 1
	except:
		degree_count[d] = 1
	if d > max_degree: 
		max_degree = d

degrees = np.empty(max_degree + 1)
nodes = np.empty(max_degree + 1)

for degree in range(0, max_degree + 1):
	degrees[degree] = degree
	try:
		nodes[degree] = degree_count[degree]
	except:
		nodes[degree] = 0

plt.plot(degrees, nodes)
plt.title('whole network degree distribution (multiple edges possible)')
plt.xlabel('degree')
plt.ylabel('number of nodes')
plt.savefig('./results/degree_distribution.png')

plt.show()

