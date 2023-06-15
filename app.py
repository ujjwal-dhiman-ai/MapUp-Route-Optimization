from flask import Flask, render_template, request
import warnings
warnings.filterwarnings("ignore")

## for data
import pandas as pd  #1.1.5
import numpy as np  #1.21.0
from tqdm import tqdm

## for plotting
import matplotlib.pyplot as plt  #3.3.2
import seaborn as sns  #0.11.1
import folium  #0.14.0
from folium import plugins
import plotly.express as px  #5.1.0
from IPython.display import display

## for simple routing
import osmnx as ox  #1.2.2
import networkx as nx  #3.0

## for advanced routing 
from ortools.constraint_solver import pywrapcp  #9.6
from ortools.constraint_solver import routing_enums_pb2
from plot_map import plot_map
app = Flask(__name__)

# Define the route for the home page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Define the route for getting the path
@app.route('/get_path', methods=['POST'])
def get_path():
    start_point = str(request.form['start_point'])
    end_point = str(request.form['end_point'])

    # print(type(start_point))
    df = pd.read_csv("50_sampled.csv")

    # print(type(df["name"][0]))
    # print(start_point)
    # print(df['name'][0])
    # print(start_point == df["name"][0])
    # if(len(df) == 0): print("Data is not properly read")
    # else: print("Data read successfully", len(df))

    df['id'] = range(50)
    col_order = ['id','y','x','amenity','name']
    df = df.reindex(columns=col_order)

    # pinpoint your starting location
    i = start_point
    df["base"] = df["name"].apply(lambda x: 1 if x==i else 0)

    # print(df.head(3))
    start = df[df["base"]==1][["y","x"]].values[0]


    # create network graph
    G = ox.graph_from_point(start, dist=10000, network_type="drive")  #'drive', 'bike', 'walk'
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    ## DIJKSTRA ALGORITHM

    df["node"] = df[["y","x"]].apply(lambda x: ox.distance.nearest_nodes(G, x[1], x[0]), axis=1)
    df = df.drop_duplicates("node", keep='first')
    # df.head()

    start_node = df.loc[df['name'] == start_point, 'node'].values[0]
    end_node = df.loc[df['name'] == end_point, 'node'].values[0]

    path_lenght = nx.shortest_path(G, source=start_node, target=end_node,method='dijkstra', weight='lenght')   

    path_time = nx.shortest_path(G, source=start_node, target=end_node,method='dijkstra', weight='travel_time')   

    '''print('Red  route:',round(sum(ox.utils_graph.get_route_edge_attributes(G,path_lenght,'length'))/1000, 2),'km |',
        round(sum(ox.utils_graph.get_route_edge_attributes(G,path_lenght,'travel_time'))/60, 2),'min')

    print('Blue route:',round(sum(ox.utils_graph.get_route_edge_attributes(G,path_time,'length'))/1000, 2),'km |',
        round(sum(ox.utils_graph.get_route_edge_attributes(G,path_time,'travel_time'))/60, 2),'min')'''
    
    time_output = 'Blue route: {:.2f} km | {:.2f} min'.format(
    round(sum(ox.utils_graph.get_route_edge_attributes(G, path_time, 'length')) / 1000, 2),
    round(sum(ox.utils_graph.get_route_edge_attributes(G, path_time, 'travel_time')) / 60, 2))

    length_output = 'Red route: {:.2f} km | {:.2f} min'.format(
    round(sum(ox.utils_graph.get_route_edge_attributes(G, path_lenght, 'length')) / 1000, 2),
    round(sum(ox.utils_graph.get_route_edge_attributes(G, path_lenght, 'travel_time')) / 60, 2))

    output = length_output + "\n" + time_output

    
    map_ = plot_map(df, y="y", x="x", start=start, zoom=12,tiles="cartodbpositron", popup="name", color="base", lst_colors=["black","red"])

    ox.plot_route_folium(G, route=path_lenght, route_map=map_, color="red", weight=1)
    ox.plot_route_folium(G, route=path_time, route_map=map_, color="blue", weight=1)
    
    # map_path = "templates/map.html"
    map_path = "G:/Shared drives/common/personal-folders-team/Ujjwal-Dhiman/data-training/route-optimization-challenge/04_python_scripts/templates/map.html"
    map_.save(map_path)
    print("Map saved successfully for: ", start_point, "--->", end_point)
    
    return render_template('index.html', output = output)

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run()
