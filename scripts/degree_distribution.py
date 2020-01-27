import collections
from matplotlib import pyplot
import numpy as np

# local modules
import network_loader

network = network_loader.load()

degree_count = {}
max_degree = 0
for n, d in network.degree():
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

pyplot.plot(degrees, nodes)
pyplot.title('whole network degree distribution (multiple edges possible)')
pyplot.xlabel('degree')
pyplot.ylabel('number of nodes')
pyplot.savefig('./results/degree_distribution.png')

pyplot.show()

