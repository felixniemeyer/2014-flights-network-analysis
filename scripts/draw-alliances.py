import networkx as nx
import plotly.graph_objects as go

# local modules 
from network_loaders import loadAirlineNetwork

alliances = {}
joint = None 

alliance_names = ['oneworld', 'skyteam', 'staralliance', 'vanilla']

for alliance_name in alliance_names:
	print(alliance_name)
	f = open("../data/alliances/" + alliance_name)

	alliance = None
	for airline_id in map(lambda line: line.strip(), f): 
		S = loadAirlineNetwork(airline_id)
		if alliance == None:
			alliance = S
		else: 
			alliance = nx.compose(alliance, S) 

	alliances[alliance_name] = alliance

	if joint == None: 
		joint = alliance
	else: 	
		joint = nx.compose(joint, alliance) 

fig = go.Figure()
lons = []
lats = []
texts = []
for airport_id in joint.nodes: 
	airport = joint.nodes[airport_id]
	lons.append(airport["longitude"])
	lats.append(airport["latitude"])
	texts.append(airport["name"])

fig.add_trace(go.Scattergeo(
	lon=lons,
	lat=lats,
	marker=dict(
		size=2, 
		color='rgb(55,55,55)'
	),
	name="airports"
))

color = dict(
	oneworld = 'rgb(155,0,105)',
	skyteam = 'rgb(5,14,155)',
	staralliance = 'rgb(105,105,105)', 
	vanilla = 'rgb(160,160,0)'
)

for alliance_name in alliance_names:
	alliance = alliances[alliance_name]
	lons = []
	lats = []
	for edge in alliance.edges: 
			sa = alliance.nodes[edge[0]]
			da = alliance.nodes[edge[1]]
			lons = lons + [sa["longitude"], da["longitude"], None]
			lats = lats + [sa["latitude"], da["latitude"], None]
	
	fig.add_trace(go.Scattergeo(
		lon=lons,
		lat=lats,
		mode='lines',
		line=dict(
			width=1, 
			color=color[alliance_name],
		),
		opacity=0.5,
		name=alliance_name
	))

fig.update_layout(
	geo=go.layout.Geo(),
	height=900
)
fig.update_geos(
	resolution=110, 
	projection_type='natural earth'
)

fig.show()
