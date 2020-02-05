import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
import geopy.distance

# local modules
import local_config

def getEntireNetwork():
	routes = nx.MultiDiGraph()
	conn = sqlite3.connect(local_config.db_file)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM routes limit 100")
	rows = cursor.fetchall()

	def get_dist(orig, dest):
		coord = []
		cursor.execute("SELECT * from airports WHERE iata=? OR iata=?", (dest, orig))
		airports = cursor.fetchall()
		for airport in airports:
			coord.append((airport[6], airport[7]))
		if len(airports) == 2:
			return geopy.distance.vincenty(coord[0], coord[1]).km
		else:
			return 100  # just a random distance when sometimes we dont have the coords of the airport

	for row in rows:
		if not routes.has_edge(row[2], row[4], key=row[1]):
			dist = get_dist(row[2], row[4])
			routes.add_edge(row[2], row[4], key=row[1], dist=dist)

	nx.draw_networkx(routes, with_labels=True, node_size=10, font_size=2, arrowsize=4)
	plt.savefig("./sample3.pdf", bbox_inches='tight', format='pdf', dpi=1200)
	return routes

def loadAirlineNetwork(airline_id):
	G = nx.DiGraph()
	conn = sqlite3.connect(local_config.db_file)
	cursor = conn.cursor()

	route_columns = [
		"source_airport_id", 
		"destination_airport_id", 
		"airline_id",
		"geo_distance", 
		"passenger_flow"
	]

	query = "SELECT {} FROM routes WHERE airline_id=?".format(', '.join(route_columns))

	cursor.execute(query, [airline_id])

	for row in cursor: 
		sa_id = row[0]
		da_id = row[1]
		attribs = {}
		for column_name in route_columns[2:]:
			attribs[column_name] = column_name
		G.add_edge(sa_id, da_id, attr_dict=attribs)

	return G
