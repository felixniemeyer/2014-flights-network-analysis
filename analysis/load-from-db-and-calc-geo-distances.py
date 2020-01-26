import sqlite3
import geopy.distance

#local modules
import db_config 

def load():
	db_conn = sqlite3.connect(db_config.db_file)
	db_cursor = db_conn.cursor()


	airport_columns = [
		"airport_id",
		"name", 
		"iata", 
		"icao", 
		"city", 
		"country", 
		"latitude", 
		"longitude", 
		"patronage",
	]
	db_cursor.execute('SELECT {0} FROM airports'.format(', '.join(airport_columns)))
	airports = {}
	for row in db_cursor:
		airport_id = row[0]
		airports[airport_id] = {}
		column_index = 1
		for column_name in airport_columns[1:]: 
			airports[airport_id][column_name] = row[column_index]
			column_index += 1

	airline_columns = [
		"airline_id", 
		"name",
		"iata", 
		"icao"
	]
	db_cursor.execute('SELECT {0} FROM airlines'.format(', '.join(airline_columns)))
	airlines = {}
	for row in db_cursor:
		airline_id = row[0]
		airlines[airline_id] = {}
		column_index = 1
		for column_name in airline_columns[1:]: 
			airlines[airline_id][column_name] = row[column_index]
			column_index += 1

	route_columns = [
		"airline_id",
		"source_airport_id",
		"destination_airport_id"
	]
	db_cursor.execute('SELECT {0} FROM routes'.format(', '.join(route_columns)))
	routes = []
	for row in db_cursor:
		route = {}
		column_index = 0
		for column_name in route_columns: 
			route[column_name] = row[column_index]
			column_index += 1
		route["geo_distance_in_km"] = get_airports_geo_distance(
			airports[route["source_airport_id"]], 
			airports[route["destination_airport_id"]]
		)
		routes.append(route)
	
	return routes, airlines, airports


def get_airports_geo_distance(airportA, airportB):
	coordsA = [airportA["latitude"], airportA["longitude"]]
	coordsB = [airportB["latitude"], airportB["longitude"]]
	return geopy.distance.geodesic(coordsA, coordsB).km

