import networkx as nx
import sqlite3

# local modules
import local_config

def load(): 
	conn = sqlite3.connect(local_config.db_file) 
	cursor = conn.cursor()

	route_columns = [
		"airline_id",
		"source_airport_id",
		"destination_airport_id",
		"geo_distance",
	]
	cursor.execute("""
	SELECT
		%s
	FROM 
		routes 
	""" % ', '.join(route_columns))

	routes = []
	for row in cursor:
		route = {}
		for i, column_name in enumerate(route_columns):
			route[column_name] = row[i]
		routes.append(route)

	network = nx.MultiDiGraph()
	for route in routes:
		network.add_edge(route["source_airport_id"], route["destination_airport_id"])

	return network

