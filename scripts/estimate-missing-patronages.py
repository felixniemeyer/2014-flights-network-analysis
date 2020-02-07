import sqlite3
import sys
import networkx as nx

# local modules
import network_loaders 

if len(sys.argv) < 3: 
	print("Usage: {0} <db-file> <output-file>".format(sys.argv[0]))
else:

	G = network_loaders.loadEntireNetwork(
		airport_columns=["patronage"],
		route_columns=[], 
		db_file=sys.argv[1]
	)

	G = G.to_undirected(reciprocal=False)

	nodes = G.nodes

	of = open(sys.argv[2], 'w') 

	previous_remaining = -1
	remaining = 0
	while remaining != previous_remaining:
		previous_remaining = remaining
		remaining = 0
		estimated_patronages = {}
		for airport_id in nodes:
			node = nodes[airport_id]
			if node["patronage"] == None:
				neighbors = G.neighbors(airport_id) 
				node_degree = G.degree(airport_id)
				estimation_sum = 0
				count = 0
				for neighbor_id in neighbors: 
					neighbor = nodes[neighbor_id]
					if neighbor["patronage"] != None: 
						estimation_sum += node_degree * neighbor["patronage"] / G.degree(neighbor_id)
						count += 1
				if count == 0:
					remaining += 1
				else:
					estimation_avg = estimation_sum / count
					estimated_patronages[airport_id] = estimation_avg
		for airport_id in estimated_patronages: 
			nodes[airport_id]["patronage"] = estimated_patronages[airport_id]
			line = "%s,%i\n" % (airport_id, estimated_patronages[airport_id])
			of.write(line)
			#print(line)
	
	of.flush()	
