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
		airport.recalc_flow_sum_and_deviation()

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

		i += 1	
		parent += add_to_parent
		add_to_parent = (add_to_parent + 1) % 2
		left += 2


	p = 0.9
	for iteration in range(0,len(airport_list)):
	 	# root.worst.rec_print(max_depth=4) 
		pivot = root.worst
		f = math.pow(pivot.flow_sum / pivot.patronage, p) * pivot.patronage - pivot.flow_sum

		pivot.rec_print(3)
		print('f:', f)

		affected_airports = set([pivot])
		for route in pivot.in_routes + pivot.out_routes: 
			affected_airports.add(route.destination_airport) 
			affected_airports.add(route.source_airport) 
			print('route flow, weight', route.flow, route.flow / pivot.flow_sum)
			route.flow = max(1, route.flow + route.flow / pivot.flow_sum * f)
			print('route flow after', route.flow)
		
		print('affected airports', affected_airports)

		for airport in affected_airports:
			airport.recalc_flow_sum_and_deviation()
			airport.bubble()

		p *= 0.9

		input()
		
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
