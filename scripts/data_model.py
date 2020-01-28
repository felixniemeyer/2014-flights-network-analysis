import math
import random

class Route: 
	def __init__(self, airline, source_airport, destination_airport, geo_distance, flow=0):
		self.airline = airline
		self.source_airport = source_airport
		self.destination_airport = destination_airport
		self.geo_distance = geo_distance
		self.flow = flow
		self.flow_delta = 0

class Airport: 
	def __init__(self, airport_id, name, iata, icao, city, country, latitude, longitude, patronage):
		self.airport_id = airport_id
		self.name = name
		self.iata = iata
		self.icao = icao
		self.city = city
		self.country = country
		self.latitude = latitude
		self.longitude = longitude
		self.patronage = patronage
		self.in_routes = []
		self.out_routes = []
		self.flow_deviation = 0
		self.flow_sum = 0
		self.degree = 0

	def recalc_flow_sum(self): 
		routes = self.in_routes + self.out_routes
		self.flow_sum = 0
		for route in routes: 
			self.flow_sum += route.flow

	def recalc_flow_sum_and_deviation(self): 
		self.recalc_flow_sum()
		self.recalc_flow_deviation()
	
	def recalc_flow_deviation(self): 
		self.flow_deviation = math.log(self.flow_sum/self.patronage)

	def __repr__(self): 
		return "%s: %s\nflow_deviation: %f\n" % ( self.airport_id, self.name, self.flow_deviation ) 


class Airline: 
	def __init__(self, airline_id, name, iata, icao): 
		self.airline_id = airline_id
		self.name = name
		self.iata = iata
		self.icao = icao
