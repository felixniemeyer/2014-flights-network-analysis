import csv
import networkx as nx
import matplotlib.pyplot as plt

def loadNetwork():

	routes = nx.MultiDiGraph()

	with open('../data/routes.dat') as f: 
		csv_reader = csv.reader(f)
		for row in csv_reader: 
			routes.add_edge(row[3], row[5]) 
	
	return routes
