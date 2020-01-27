import math

class Route: 
	def __init__(self, airline, source_airport, destination_airport, geo_distance, flow=0):
		self.airline = airline
		self.source_airport = source_airport
		self.destination_airport = destination_airport
		self.geo_distance = geo_distance
		self.flow = flow

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
		self.degree = 0
		# references for the heap
		self.l = None
		self.r = None
		self.p = None

	def recalc_flow_deviation(self): 
		routes = self.in_routes + self.out_routes
		flow_sum = 0
		for route in routes: 
			flow_sum += route.flow
		self.flow_deviation = math.log(flow_sum/self.patronage)

	def __repr__(self): 
		return """
%s
flow_deviation: %f """ % ( self.name, self.flow_deviation ) 

class Airline: 
	def __init__(self, airline_id, name, iata, icao): 
		self.airline_id = airline_id
		self.name = name
		self.iata = iata
		self.icao = icao
