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

start_point = str(input("Enter starting point: "))
end_point = str(input("Enter ending point: "))

df = pd.read_csv("G:/Shared drives/common/personal-folders-team/Ujjwal-Dhiman/data-training/route-optimization-challenge/50_sampled.csv")
df['id'] = range(50)
col_order = ['id','y','x','amenity','name']
df = df.reindex(columns=col_order)


# pinpoint your starting location
i = 0
df["base"] = df["id"].apply(lambda x: 1 if x==i else 0)
start = df[df["base"]==1][["y","x"]].values[0]

# print("start =", start)
# df.head(3)

def plot_map(df, y, x, start, zoom=12, tiles="cartodbpositron", popup=None, size=None, color=None, legend=False, lst_colors=None, marker=None):
    data = df.copy()

    ## create columns for plotting
    if color is not None:
        lst_elements = sorted(list(df[color].unique()))
        lst_colors = ['#%06X' % np.random.randint(0, 0xFFFFFF) for i in range(len(lst_elements))] if lst_colors is None else lst_colors
        data["color"] = data[color].apply(lambda x: lst_colors[lst_elements.index(x)])

    if size is not None:
        scaler = preprocessing.MinMaxScaler(feature_range=(3,15))
        data["size"] = scaler.fit_transform(data[size].values.reshape(-1,1)).reshape(-1)

    ## map
    map_ = folium.Map(location=start, tiles=tiles, zoom_start=zoom)

    if (size is not None) and (color is None): 
        data.apply(lambda row: folium.CircleMarker(location=[row[y],row[x]], popup=row[popup],
                                                   color='#3186cc', fill=True, radius=row["size"]).add_to(map_), axis=1)
    elif (size is None) and (color is not None):
        data.apply(lambda row: folium.CircleMarker(location=[row[y],row[x]], popup=row[popup],
                                                   color=row["color"], fill=True, radius=5).add_to(map_), axis=1)
    elif (size is not None) and (color is not None):
        data.apply(lambda row: folium.CircleMarker(location=[row[y],row[x]], popup=row[popup],
                                                   color=row["color"], fill=True, radius=row["size"]).add_to(map_), axis=1)
    else:
        data.apply(lambda row: folium.CircleMarker(location=[row[y],row[x]], popup=row[popup],
                                                   color='#3186cc', fill=True, radius=5).add_to(map_), axis=1)
    
    ## tiles
    layers = ["cartodbpositron", "openstreetmap", "Stamen Terrain", 
              "Stamen Water Color", "Stamen Toner", "cartodbdark_matter"]
    for tile in layers:
        folium.TileLayer(tile).add_to(map_)
    folium.LayerControl(position='bottomright').add_to(map_)
    
    ## legend
    if (color is not None) and (legend is True):
        legend_html = """<div style="position:fixed; bottom:10px; left:10px; border:2px solid black; z-index:9999; font-size:14px;">&nbsp;<b>"""+color+""":</b><br>"""
        for i in lst_elements:
            legend_html = legend_html+"""&nbsp;<i class="fa fa-circle fa-1x" style="color:"""+lst_colors[lst_elements.index(i)]+""""></i>&nbsp;"""+str(i)+"""<br>"""
        legend_html = legend_html+"""</div>"""
        map_.get_root().html.add_child(folium.Element(legend_html))
    
    ## add marker
    if marker is not None:
        lst_elements = sorted(list(df[marker].unique()))
        lst_colors = ["black","red","blue","green","pink","orange","gray"]  #7
        ### too many values, can't mark
        if len(lst_elements) > len(lst_colors):
            raise Exception("marker has uniques > "+str(len(lst_colors)))
        ### binary case (1/0): mark only 1s
        elif len(lst_elements) == 2:
            data[data[marker]==lst_elements[1]].apply(lambda row: folium.Marker(location=[row[y],row[x]], popup=row[marker], draggable=False, 
                                                                                icon=folium.Icon(color=lst_colors[0])).add_to(map_), axis=1) 
        ### normal case: mark all values
        else:
            for i in lst_elements:
                data[data[marker]==i].apply(lambda row: folium.Marker(location=[row[y],row[x]], popup=row[marker], draggable=False, 
                                                                      icon=folium.Icon(color=lst_colors[lst_elements.index(i)])).add_to(map_), axis=1)
    
    ## full screen
    plugins.Fullscreen(position="topright", title="Expand", title_cancel="Exit", force_separate_button=True).add_to(map_)
    return map_



## SHORTEST PATH BETWEEN TWO NODES

# we are considering the road network as a graph and find the shortest path between nodes.

# create network graph
G = ox.graph_from_point(start, dist=10000, network_type="drive")  #'drive', 'bike', 'walk'
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# plot
# fig, ax = ox.plot_graph(G, bgcolor="black", node_size=0, node_color="white", figsize=(16,8))

# nodes_df = ox.graph_to_gdfs(G, nodes=True, edges=False).reset_index()

# links_df = ox.graph_to_gdfs(G, nodes=False, edges=True).reset_index()

## DIJKSTRA ALGORITHM

df["node"] = df[["y","x"]].apply(lambda x: ox.distance.nearest_nodes(G, x[1], x[0]), axis=1)
df = df.drop_duplicates("node", keep='first')
# df.head()

start_node = df.loc[df['name'] == start_point, 'node'].values[0]
end_node = df.loc[df['name'] == end_point, 'node'].values[0]

# end = df[df["id"]==15][["y","x"]].values[0]
# print("locations: from", start, "--> to", end)

# start_node = ox.distance.nearest_nodes(G, start[1], start[0])
# end_node = ox.distance.nearest_nodes(G, end[1], end[0])
# print("nodes: from", start_node, "--> to", end_node)

# calculate shortest path using dijkstra algorithm
path_lenght = nx.shortest_path(G, source=start_node, target=end_node, 
                                method='dijkstra', weight='lenght')     
# print(path_lenght)

# plot on the graph
''' fig, ax = ox.plot_graph_route(G, path_lenght, route_color="red", 
                              route_linewidth=5, node_size=1, 
                              bgcolor='black', node_color="white", 
                              figsize=(16,8))'''

# calculate shortest path optimized for time
path_time = nx.shortest_path(G, source=start_node, target=end_node, 
                                method='dijkstra', weight='travel_time')   
# print(path_time)

# plot on the graph
'''fig, ax = ox.plot_graph_route(G, path_time, route_color="blue", 
                              route_linewidth=5, node_size=1, 
                              bgcolor='black', node_color="white", 
                              figsize=(16,8))'''

# plot on the map to compare both paths
# display data points as locations on a map using folium

map_ = plot_map(df, y="y", x="x", start=start, zoom=12, 
                tiles="cartodbpositron", popup="id", 
                color="base", lst_colors=["black","red"])

ox.plot_route_folium(G, route=path_lenght, route_map=map_, 
                     color="red", weight=1)
ox.plot_route_folium(G, route=path_time, route_map=map_, 
                     color="blue", weight=1)
# map_   
# Display the map in the Python terminal
# display(map_._repr_html_())               

map_.save("map.html")

print("Map saved successfully.........")