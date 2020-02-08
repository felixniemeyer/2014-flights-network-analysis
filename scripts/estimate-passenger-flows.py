import math
from functools import reduce
from queue import PriorityQueue
from matplotlib import pyplot
import numpy
import sys

#local modules
import load_from_db
import local_config

def run(db_file): 
	(routes, airlines, airports) = load_from_db.load(db_file)

	#initialize flows
	for route in routes: 
		route.destination_airport.in_routes.append(route) 
		route.source_airport.out_routes.append(route) 

	for i, airport in airports.items(): 
		airport.degree = len(airport.in_routes) + len(airport.out_routes)
		for route in airport.get_routes(): 
			alid = route.airline.airline_id
			try: 
				airport.airline_degree[alid] += 1
			except: 
				airport.airline_degree[alid] = 1

	print()
	for i, route in enumerate(routes): 
		sa = route.source_airport
		da = route.destination_airport
		total_flow = math.sqrt(da.patronage / da.degree * sa.patronage / sa.degree) 

		share_sum = 0
		this_share = 0
		count = 0
		for r in sa.out_routes: 
			if r.destination_airport == da: 
				count += 1
				alid = r.airline.airline_id
				share = math.sqrt(
					r.source_airport.airline_degree[alid] * 
					r.destination_airport.airline_degree[alid]
				)
				share_sum += share
				if r == route: 
					this_share = share
		route.flow = total_flow * count * this_share / share_sum

		sys.stdout.write("\rinitializing {0:.1f}%".format(100 * i / len(routes)))
	sys.stdout.write("\rinitializing 100%   \n")

	for i, airport in airports.items(): 
		airport.recalc_flow_sum_and_deviation()

	if script_mode == "show": 
		min_max_sum = plot_flow_deviation_distribution(airports)
		labels = ["initial. min, max, sum: [{0:.2f}, {1:.2f}, {2:.2f}]".format(*min_max_sum)]

	iterations = 120
	plot_each = iterations / 12
	last_plot = -1
	factor = math.pow(0.9, 1 / iterations) 
	p = 0
	for iteration in range(0, iterations):
		for i, airport in airports.items():
			target_flow_sum = math.pow(airport.flow_sum / airport.patronage, p) * airport.patronage
			f = target_flow_sum  - airport.flow_sum
			for route in airport.in_routes + airport.out_routes: 
				route.flow_delta += route.flow / airport.flow_sum * f

		for route in routes:
			route.flow = max(1, route.flow + route.flow_delta)
			route.flow_delta = 0

		for i, airport in airports.items():
			airport.recalc_flow_sum_and_deviation()
		
		if iteration - last_plot >= plot_each: 
			last_plot = iteration 
			
			if script_mode == "show":
				min_max_sum = plot_flow_deviation_distribution(airports)
				label_template = "iteration {3}. min, max, sum(abs): [{0:.2f}, {1:.2f}, {2:.2f}]"
				labels.append(label_template.format(*min_max_sum, iteration + 1))

		sys.stdout.write("\riterating {0:.1f}%".format(100 * (iteration / iterations)))

		p = 1 - (1 - p) * factor

	sys.stdout.write("\riterating 100%   \n")

	if script_mode == "show": 
		pyplot.title("deviation")
		pyplot.legend(labels, loc=2)
		pyplot.xlabel('nodes , ordered by flow_deviation')
		pyplot.ylabel('flow_deviation $ln(FlowSum(n)/FlowDeviation(n))$')
		pyplot.savefig(
			'./results/flow_estimation_{0}_iterations.png'.format(iterations),
			dpi=300
			bbox_inches='tight'
		)
		pyplot.show()

	if script_mode == "write_csv":
		routes_csv = open('./temp_passenger_flows.csv', 'w')
		for route in routes: 
			routes_csv.write("%s,%s,%s,%f\n" % (
				route.airline.airline_id,
				route.source_airport.airport_id,
				route.destination_airport.airport_id,
				route.flow
			))
		airport_csv = open('./temp_flow_estimation_metrics.csv', 'w')
		for airport_id, airport in airports.items():
			airport_csv.write("%s,%f,%f\n" % (
				airport_id, 
				airport.flow_sum, 
				airport.flow_deviation
			))
		routes_csv.flush()
		airport_csv.flush()

def plot_flow_deviation_distribution(airports):
	airport_generator = map(lambda t: t[1], airports.items())
	sorted_list = sorted(airport_generator, key=lambda airport: airport.flow_deviation)
	data = numpy.empty(len(sorted_list))
	i = 0
	abs_integral = 0
	for airport in sorted_list:
		data[i] = airport.flow_deviation
		abs_integral += abs(airport.flow_deviation)
		i += 1

	pyplot.plot(data)
	smallest = sorted_list[0].flow_deviation
	highest = sorted_list[-1].flow_deviation
	return (smallest, highest, abs_integral )

understood = True
if len(sys.argv) < 2: 
	script_mode = "show"
else: 	
	script_mode = sys.argv[1]
	if script_mode not in ["show", "write_csv"]:
		understood = False

if len(sys.argv) < 3: 
	db_file = local_config.db_file
else:
	db_file = sys.argv[2]

if understood:
	run(db_file)
else:
	print("Error: wrong usage.")
	print("Correct usage: {0} <mode=show|write_csv> [<db_file>]".format(sys.argv[0])) 
