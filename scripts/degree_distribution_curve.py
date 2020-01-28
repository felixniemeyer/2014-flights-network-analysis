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

def f1(x, c, a):
	return c * np.power(math.e, -a * x)

def f2(x, c, g):
	return c * np.power(x, -g)

f = f2

((c, a), pcov) = scipy.optimize.curve_fit(f, (degrees), (nodes), p0=(100,0.5))
 
x = np.logspace(0,np.log10(max_degree),100)
y = f(x, c, a)
 
plt.plot(degrees, nodes, 'o')
plt.plot(x, y, color='red')

plt.title('whole network degree distribution (multiple edges possible)')
plt.xlabel('degree')
plt.ylabel('number of nodes')
plt.savefig('./results/degree_distribution_curve.png')

plt.xscale('log')
plt.yscale('log')

plt.legend(['nodes per degree', '{0:.2f}*e^(-{1:.2f}d)'.format(c,a)], loc=1)

plt.show()

