import os
import sys
import networkx as nx
import concurrent.futures

# local modules
from network_loaders import loadAirlineNetwork
import largeness

alliances = {}

class Alliance: 
	def __init__(self, network, airline):
		self.network = network
		self.airlines = [airline]

	def name(self): 
		return '(%s)' % '-'.join(self.airlines)

	def merge(self, other):
		self.network = nx.compose(self.network, other.network) 
		self.airlines = self.airlines + other.airlines
		return self

	def __repr__(self): 
		return 'alliance' + self.name

def calculateOpportunity(matrix, a, b): 
	aa = alliances[a]
	ab = alliances[b]
	la = largeness.calculateForGraph(aa.network) 
	lb = largeness.calculateForGraph(ab.network) 
	c = nx.compose(aa.network, ab.network) 
	lc = largeness.calculateForGraph(c) 
	matrix[a][b] = lc / ( la + lb ) 

print('creating initial single member alliances') 
folder = "../data/alliances"
real_alliance_names = []
for f in os.listdir(folder):
	if os.path.isfile(folder + '/' + f): 
		real_alliance_names.append(f)
		print(f) 
		f = open(folder + '/' + f)
		for airline_id in map(lambda line: line.strip(), f): 
			alliance = Alliance(loadAirlineNetwork(airline_id), airline_id) 
			alliances[alliance.name()] = alliance

opportunity_matrix = {}
keys = list(alliances.keys())
tp = concurrent.futures.ThreadPoolExecutor(max_workers=7)
jobs = []
jobcount = 0
for i in keys: 
	opportunity_matrix[i] = {}
	for j in keys: 
		if i == j: 
			break
		jobs.append(tp.submit(calculateOpportunity, opportunity_matrix, i, j))
		jobcount += 1
donecount = 0
for job in concurrent.futures.as_completed(jobs):
	donecount += 1
	sys.stdout.write('\rinitialize opportunity matrix {0:.1f}%'.format(100 * donecount/jobcount))
tp.shutdown(wait=True)
print()

while len(keys) > 4: 
	highest_opportunity = 0
	hi = None
	hj = None
	for i in keys: 
		for j in keys:
			if i == j: 
				break
			if opportunity_matrix[i][j] > highest_opportunity:
				highest_opportunity = opportunity_matrix[i][j]
				hi = i
				hj = j

	print('{3} alliances left, merging {0} and {1}, opportunity = {2:.3f}'.format(
		hi, hj, highest_opportunity, len(keys) 
	))
	
	new = alliances[hi].merge(alliances[hj])
	i = new.name()
	alliances[i] = new

	del alliances[hi]
	del alliances[hj]
	
	keys.remove(hi) 
	keys.remove(hj)

	keys.append(i)

	new_opportunities = {}
	new_opportunities[i] = {}
	with concurrent.futures.ThreadPoolExecutor(max_workers=7) as tp: 
		for j in keys: 
			if i == j: 
				break
			tp.submit(calculateOpportunity, new_opportunities, i, j)

	opportunity_matrix[i] = new_opportunities[i]

result_folder = 'results/alliances'
os.makedirs(result_folder, exist_ok=True) 
for f in os.listdir(result_folder):
	os.remove(result_folder + '/' + f) 
index = 0
for key in alliances: 
	f = open(result_folder + ('/gen%i' % index), 'w')
	index += 1
	for airline_id in alliances[key].airlines: 
		f.write(airline_id + '\n') 

for key in alliances: 
	f.flush()
