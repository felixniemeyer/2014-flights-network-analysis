import sqlite3
import sys
import networkx as nx
import plotly.graph_objects as go

# local modules
import network_loaders

airport_ids = sys.argv[1:]

if len(airport_ids) > 0: 
	G = network_loaders.loadEntireNetwork()

	S = G.subgraph(airport_ids)

	fig = go.Figure()

	marker = dict(
		size=10,
		color='rgb(255,0,0)'
	)
	for airport_id in S.nodes:
		airport = S.nodes[airport_id]
		fig.add_trace(go.Scattergeo(
			lon=[float(airport["longitude"])],
			lat=[float(airport["latitude"])],
			text=airport["name"],
			mode='markers',
			marker=marker
		))

	for edge in S.edges: 
		sa = S.nodes[edge[0]]
		da = S.nodes[edge[1]]
		fig.add_trace(go.Scattergeo(
			lon=[sa["longitude"], da["longitude"]],
			lat=[sa["latitude"], da["latitude"]],
			mode='lines',
			line=dict(width=1, color='red')
		))

	fig.update_layout(
		geo=go.layout.Geo(),
		height=700
	)
	fig.update_geos(
		resolution=50, 
		projection_type='orthographic'
	)

	fig.show()
else:
	print("Usage: %s <airport_id 1> <airport_id 2> ... <airport_id n>" % sys.argv[0])
