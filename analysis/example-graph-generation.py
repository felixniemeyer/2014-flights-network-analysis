import plotly.graph_objects as go
import networkx as nx

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from IPython.display import display, Markdown
#from mpl_toolkits.mplot3d import Axes3D

options = {
    'node_color': 'lavender',
    'node_size': 300,
    'width': .1,
    'arrowstyle': '-|>',
    'arrowsize': 10,
}

options2 = {
    'node_color': 'lavender',
    'node_size': 300,
    'width': .5
}

input_data = np.array([[0, 3, 6, 0, 0], [3, 2, 4, 6, 8], [1, 0, 0, 0, 0],
                       [0, 2, 0, 0, 0], [0, 1, 0, 0, 0]])
n = input_data.shape[0]
G = nx.Graph(input_data)
mapping = dict(zip(np.arange(0, n), np.arange(1, n+1)))
G = nx.relabel_nodes(G, mapping)
nx.draw_networkx(G, **options2)
plt.show()
print('Adjacency Matrix:')
print(pd.DataFrame(input_data, index=np.arange(1, n+1), columns=np.arange(1, n+1)))
