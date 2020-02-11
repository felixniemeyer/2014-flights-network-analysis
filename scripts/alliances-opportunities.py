import networkx as nx
import sqlite3
import matplotlib.pyplot as plt
import sys

# local modules
from network_loaders import loadAirlineNetwork
import largeness

class Alliance:
	def __init__(self):
		self.airline_subgraphs = {}
		self.largeness = 0
		self.largeness_sum = 0
		self.composed = None
		pass

alliances = {}

for alliance_name in ['oneworld', 'skyteam', 'staralliance', 'vanilla']:
	print(alliance_name)
	alliance = Alliance()
	f = open("../data/alliances/" + alliance_name)
	for airline_id in map(lambda line: line.strip(), f): 
		print(airline_id)
		S = loadAirlineNetwork(airline_id)
		alliance.airline_subgraphs[airline_id] = S
		alliance.largeness_sum += largeness.calculateForGraph(S)
		if alliance.composed == None:
			alliance.composed = S
		else: 
			alliance.composed = nx.compose(alliance.composed, S) 
	alliance.largeness = largeness.calculateForGraph(alliance.composed)

	print('largeness sum', alliance.largeness_sum)
	print('alliance largeness', alliance.largeness)
	print('cooperation opportunity', alliance.largeness / alliance.largeness_sum)
	print()

	alliances[alliance_name] = alliance

