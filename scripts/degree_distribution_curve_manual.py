import collections
import matplotlib.pyplot as plt 
import numpy as np
import math
import scipy.optimize

import network_loader 

network = network_loader.load()

node_counts_dict = {}
max_degree = 0

for n, d in network.degree():
	try:
		node_counts_dict[d] += 1
	except:
		node_counts_dict[d] = 1
	if d > max_degree: 
		max_degree = d

degrees = []
node_counts = []

for degree in node_counts_dict:
	if degree % 2 == 0:
		degrees.append(degree)
		node_counts.append(node_counts_dict[degree])
	
degrees = np.array(degrees)
node_counts = np.array(node_counts) 

def f(x, c, a):
	return c * np.power(x, -a)

def f_log(x, c, a): 
	return f(np.exp(x), c, a)

# manual estimation 
mc = 4900
ma = 1.55

# least square fit
((c, a), pcov) = scipy.optimize.curve_fit(f, degrees, node_counts, p0=(100,0.5))
 
# least square fit on log
log_degrees = np.log(degrees)
((lc, la), pcov) = scipy.optimize.curve_fit(f_log, degrees, np.log(node_counts), p0=(mc, ma)) 

x = np.logspace(1,np.log10(max_degree/10),100)

plt.plot(x, f(x, c, a), color='red')
plt.plot(x, f(x, lc, la), color='green')
plt.plot(x, f(x, mc, ma), color='orange')
plt.scatter(degrees, node_counts, marker='o', s=10)

plt.xlabel('degree')
plt.ylabel('number of nodes')

plt.xscale('log')
plt.yscale('log')

labels = [
	'curve_fit: ${0:.2f}*e^{{-{1:.2f}d}}$'.format(c,a),
	'curve_fit, log(y): ${0:.2f}*e^{{-{1:.2f}d}}$'.format(lc,la),
	'manual: ${0:.2f}*e^{{-{1:.2f}d}}$'.format(mc,ma),
	'nodes per degree',
]
plt.legend(labels, loc=1)

plt.savefig('./results/degree_distribution_curve_manual.png', dpi=300, bbox_inches='tight')
plt.show()

