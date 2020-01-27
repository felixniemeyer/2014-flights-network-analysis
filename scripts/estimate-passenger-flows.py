import math
from queue import PriorityQueue
from matplotlib import pyplot
import numpy


#local modules
import load_from_db

(routes, airlines, airports) = load_from_db.load()

#initialize flows
for route in routes: 
	route.destination_airport.in_routes.append(route) 
	route.source_airport.out_routes.append(route) 

airport_list = []
for airport_id, airport in airports.items(): 
	airport.degree = len(airport.in_routes) + len(airport.out_routes)
	airport_list.append(airport)

for route in routes: 
	a = route.destination_airport.patronage / route.destination_airport.degree
	b = route.source_airport.patronage / route.source_airport.degree
	route.flow = math.sqrt(a * b) 

for airport in airport_list: 
	airport.recalc_flow_deviation()

airport_list.sort(key=lambda airport: -airport.flow_deviation)
i = 1
minimum = airport_list[0]
for airport in airport_list: 
	a = 1 << (i.bit_length() - 1)
	parent = (a >> 1) + (i >> 1) - 1
	airport.p = airport_list[parent] if parent >= 0 else None
	left = (a << 1) + (i ^ a << 1)
	airport.l = airport_list[left] if left < len(airport_list) else None
	right = left + 1
	airport.r = airport_list[right] if right < len(airport_list) else None

data = numpy.empty(len(airport_list))
for i, flow_deviation in enumerate(map(lambda airport: airport.flow_deviation, airport_list)):
	data[i] = flow_deviation

pyplot.plot(data)
pyplot.title("initial deviation") 
pyplot.show()

def rec_print(airport, depth): 
	if(depth > 0):
		print(airport) 
		rec_print(airport.r, depth - 1)
		rec_print(airport.l, depth - 1) 

rec_print(minimum, 5)

print('last\n' + airport_list[-1].__repr__())

