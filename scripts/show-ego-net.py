import sys
import networkx as nx
import matplotlib.pyplot as plt

# local modules
import network_loaders

n = '10'
if len(sys.argv) < 2: 
	print("Usage: {0} <airport_id>".format(sys.argv[0]))
	print("Now using default node {0}".format(n))
else:
	n = sys.argv[1]

G = network_loaders.loadEntireNetwork()

S = nx.ego_graph(G, n, radius=2, undirected=True) 



nx.draw(
	S,
	labels={k: "%s:\n%s\nptrn:%i\n\n\n\n" % (k, S.nodes[k]["name"], S.nodes[k]["patronage"]) for k in S.nodes},
	node_color=['#993322' if n == k else '#4477ee' for k in S.nodes],
	node_size=100
)

plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)

plt.savefig('results/ego_graph_{0}.png'.format(n), pad_inches=0.5, dpi=300)
plt.show()
