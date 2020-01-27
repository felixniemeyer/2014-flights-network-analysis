import sqlite3
import geopy.distance

#local modules
import local_config 
from data_model import Route, Airport, Airline 

def load():
	db_conn = sqlite3.connect(local_config.db_file)
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
		airports[airport_id] = Airport(*row)

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
		airlines[airline_id] = Airline(*row)
	airlines['\\N'] = Airline('\\N', 'unknown airline', '', '')

	route_columns = [
		"airline_id",
		"source_airport_id",
		"destination_airport_id",
		"geo_distance",
	]
	db_cursor.execute('SELECT {0} FROM routes'.format(', '.join(route_columns)))
	routes = []
	for row in db_cursor:
		airline = airlines[row[0]]
		source_airport = airports[row[1]]
		destination_airport = airports[row[2]]
		routes.append(Route(airline, source_airport, destination_airport, row[3]))
	
	return routes, airlines, airports

