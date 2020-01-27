import math
from queue import PriorityQueue
from matplotlib import pyplot
import numpy


#local modules
import load_from_db
from data_model import Root, Leaf

def run(): 
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

	airport_list.sort(key=lambda airport: -abs(airport.flow_deviation))

	plot_flow_deviation_distribution(airport_list)

	root = Root()
	leaf = Leaf()
	i = 1
	parent = -1
	add_to_parent = 1
	left = 1
	for airport in airport_list:
		if parent < 0: 
			airport.p = root
			root.set_worst(airport) 
		else:
			airport.p = airport_list[parent] 

		airport.l = airport_list[left] if left < len(airport_list) else leaf
		airport.r = airport_list[left+1] if left + 1 < len(airport_list) else leaf

		print('parent, left', parent, left) 
		
		i += 1	
		parent += add_to_parent
		add_to_parent = (add_to_parent + 1) % 2
		left += 2


	for iteration in range(0,len(airport_list)):
		root.worst.rec_print(max_depth=4) 
		pivot = root.worst 
		pivot.flow_deviation *= 0.1  # just for now, for debugging
		pivot.bubble()
		
	plot_flow_deviation_distribution(airport_list)
	pyplot.title("initial deviation") 
	pyplot.show()
		

def plot_flow_deviation_distribution(airport_list):
	sorted_list = sorted(airport_list, key=lambda airport: -airport.flow_deviation)
	data = numpy.empty(len(sorted_list))
	i = 0
	for airport in sorted_list:
		data[i] = airport.flow_deviation
		i += 1

	pyplot.plot(data)

run()
