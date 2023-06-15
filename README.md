# MapUp-Route-Optimization

## Summary
Route Optimization is the process of determining the most cost-efficient route. It doesn’t necessarily mean finding the shortest path between two points, as it includes all relevant factors (i.e. profit, number of locations, time windows).

## Problem Definition
This topic was first addressed mathematically in the 1930s to solve a school bus routing problem. It was called the Traveling Salesman Problem, which consists of finding the shortest way for a driver to visit all the locations, given the distances between them.

The Traveling Salesman Problem can be generalized into the Vehicle Routing Problem: the issue of mapping routes for vehicles while minimizing an objective function composed of operating costs and user preferences. It’s the main problem in logistics transportation. For instance, if at night there is a lot of traffic (or high tolls) on the shortest path, it might not be the optimal route for dinner deliveries.
Data
Here we used data for taxi stands in singapore. After cleaning the raw data we are left with data which contain 4 columns. Data Dictionary -

Latitude
Latitudes are horizontal lines that measure distance north or south of the equator. 
Longitude
Longitudes are vertical lines that measure east or west of meridian in Greenwich, England.
Amenity
In this project we are working on only taxi stands, so under this column amenity type will be taxi.
Name
This specifies the name of each taxi stand.




Source: https://overpass-turbo.eu/s/1w4p  

Data:https://docs.google.com/spreadsheets/d/12lcKCOOsf4Ob2xiAwyRgEvRTgrHwiXBEvMVSlkGtSj8/edit#gid=0

## Proposed Solution
This project is Python based and uses the Flask web framework to create a web application for finding the shortest path between two points on a map. The application takes input from the user for the starting and ending points, and then it reads a dataset containing information about various locations.

The script uses the OSMnx library to retrieve a road network graph from OpenStreetMap based on the starting point. It calculates the shortest path between the starting and ending points using Dijkstra's algorithm, considering both the length and travel time of the edges.

The project also includes code for plotting the map and the shortest paths using various visualization libraries such as Folium, Matplotlib, and Plotly. It generates an HTML map with the shortest paths highlighted in red and blue.

When the user submits the form with the starting and ending points, the script processes the request, performs the path calculations, and saves the resulting map as an HTML file. The file path of the generated map is then returned as the response to the user.

In summary, this project aims to create a web application that allows users to find the shortest path between two points on a map. It utilizes OSMnx and various plotting libraries to calculate and visualize the paths.



## Implementation

File Structure:

route-optimization
- app.py
- plot_map.py
- sample.py
- 50_sampled.csv
- templates
 - index.html
 - map.html


1. app.py: This is the main Flask application file. It defines the routes for the home page ("/") and the route to get the optimized path ("/get_path"). The get_path() function reads a CSV file containing location data, performs network analysis, calculates the shortest paths using the Dijkstra algorithm, and generates a map with the routes. The map is saved as an HTML file and rendered in the index.html template.

2. sample.py: This code is used to sample a specific number of data points from a given CSV file.

3. plot_map.py: This code defines a function called plot_map that generates an interactive map using various Python libraries such as folium, matplotlib, and seaborn. The purpose of the function is to plot geographical data on a map and customize the visual representation based on specified parameters.

4. index.html: This HTML template file defines the structure of the web page. It includes a form with dropdown menus to select the start and end points, a button to trigger the route optimization, and a section to display the output and the map. JavaScript code can be added to this file for additional functionality.

5. map.html: This file is dynamically generated by the app.py file and contains the interactive map with the optimized routes.



To run the Flask web application, you need to execute the app.py file. The application will start a local server, and you can access it by opening a web browser and navigating to the specified address (usually http://localhost:5000/).

Please note that the provided code assumes the presence of a CSV file named "50_sampled.csv" in the specified location. Additionally, you may need to install the required Python libraries using pip or conda before running the application.

## Further Improvements
The web application can also be hosted on a web server like, streamlit. We can also use github pages to host this application online.
