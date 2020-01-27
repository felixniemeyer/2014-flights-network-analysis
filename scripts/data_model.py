import math
import random

class Route: 
	def __init__(self, airline, source_airport, destination_airport, geo_distance, flow=0):
		self.airline = airline
		self.source_airport = source_airport
		self.destination_airport = destination_airport
		self.geo_distance = geo_distance
		self.flow = flow

class Root: 
	def __init__(self): 
		self.worst = None 

	def better_than(self, other): 
		return False

	def set_worst(self, worst): 
		self.worst = worst

	def replace_child(self, child, new):
		print('ho') 
		if(self.worst == child):
			print('ha') 
			self.worst = new

	def rec_print(self): 
		if self.worst != None: 
			self.worst.rec_print()

class Leaf: 
	def __init__(self): 
		self.flow_deviation = 0

	def set_parent(self, new): 
		pass

	def rec_print(self): 
		pass
	
	def better_than(self, other):
		return True

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
		# references for the heap
		self.l = None
		self.r = None
		self.p = None

	def recalc_flow_sum(self): 
		routes = self.in_routes + self.out_routes
		self.flow_sum = 0
		for route in routes: 
			self.flow_sum += route.flow
		print('new flow sum', self.flow_sum)

	def recalc_flow_sum_and_deviation(self): 
		self.recalc_flow_sum()
		self.recalc_flow_deviation()
	
	def recalc_flow_deviation(self): 
		self.flow_deviation = math.log(self.flow_sum/self.patronage)

	def bubble(self):
		# print('bubbling\n', self, self.l, self.r)
		self.bubble_up()
		self.bubble_down()

	def bubble_up(self):
		if self.p.better_than(self):
			if(self.p.l == self):
				self.p.switch(True) 
				self.bubble_up()
			else:
				self.p.switch(False) 
				self.bubble_up()

	def bubble_down(self):
		if self.l.better_than(self.r): 
			if self.better_than(self.r):
				self.switch(False)
				self.bubble_down()
		else:
			if self.better_than(self.l): 
				self.switch(True)
				self.bubble_down() 

	def rec_print(self, max_depth=None, ident = ""): 
		if max_depth != None:
			max_depth -= 1
			if max_depth < 0:
				return 
		print(ident, self) 
		ident += "  "
		self.l.rec_print(max_depth, ident) 
		self.r.rec_print(max_depth, ident)

	def switch(self, left):
		if left: 
			child = self.l
			sibling = self.r
		else:
			child = self.r
			sibling = self.l

		self.r = child.r
		self.l = child.l
		self.p.replace_child(self, child) 
		child.r.set_parent(self)
		child.l.set_parent(self)
		child.p = self.p
		self.p = child
		sibling.set_parent(child) 

		if left: 
			child.r = sibling
			child.l = self
		else:
			child.r = self
			child.l = sibling
		
	def replace_child(self, child, new):
		if(self.l == child):
			self.l = new
		if(self.r == child): 
			self.r = new

	def set_parent(self, new): 
		self.p = new
	
	def better_than(self, other):
		return abs(self.flow_deviation) < abs(other.flow_deviation)

	def __repr__(self): 
		return "%s: %s\nflow_deviation: %f\n" % ( self.airport_id, self.name, self.flow_deviation ) 


class Airline: 
	def __init__(self, airline_id, name, iata, icao): 
		self.airline_id = airline_id
		self.name = name
		self.iata = iata
		self.icao = icao
