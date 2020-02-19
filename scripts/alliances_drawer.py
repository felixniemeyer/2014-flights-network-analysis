import os
import networkx as nx
import plotly.graph_objects as go

# local modules 
from network_loaders import loadAirlineNetwork

def drawAlliances(folder = "../data/alliances"):
	print(folder) 
	alliance_names = []
	for f in os.listdir(folder):
		if os.path.isfile(folder + '/' + f): 
			alliance_names.append(f)
			print('found airline', f) 

	alliances = {}
	joint = None 

	for alliance_name in alliance_names:
		f = open(folder + "/" + alliance_name)

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

	colors = [ 
		'rgb(155,0,105)',
		'rgb(185,140,5)', 
		'rgb(5,14,155)',
		'rgb(90,160,0)'
	]
	color_index = 0
	for i, alliance_name in enumerate(alliance_names):
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
				width=0.45, 
				color=colors[i % len(colors)],
			),
			opacity=0.4,
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
