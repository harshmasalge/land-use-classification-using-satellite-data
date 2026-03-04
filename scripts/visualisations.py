import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

import geodatasets
import folium
import matplotlib.pyplot as plt
import os,json
import contextily as cx
from shapely.geometry import box
import geemap
 

# airshed_path = 'data/raw/delhi_airshed.geojson'

# airshed_dict = json.load(open(airshed_path))

# coordinates_list = airshed_dict['features'][0]['geometry']['coordinates'][0]
# # print(coordinates_list)
# coordinates_array = np.array(coordinates_list)
# # print(coordinates_array.shape)

# # Plotting the coordinates
# plt.figure(figsize=(10, 10))
# plt.plot(coordinates_array[:, 0], coordinates_array[:, 1],  color='blue')
# plt.title('Airshed Boundary')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.grid()
# plt.show()


# def plot_airshed(path, title='Airshed'):
#     # Load the shapefile using geopandas
#     gdf = gpd.read_file(path)
#     # print(gdf)  # Print the first few rows of the GeoDataFrame to check the data

#     # Plot the shapefile
#     fig, ax = plt.subplots(figsize=(10, 10))
#     gdf.plot(ax=ax, color='lightblue', alpha=0.5, edgecolor='black')

#     # Set title and labels
#     ax.set_title(title)
#     ax.set_xlabel('Longitude')
#     ax.set_ylabel('Latitude')
#     ax.grid()

#     # Show the plot
#     plt.show()
#     return ax


# airshed_path = 'data/raw/delhi_airshed.geojson'

# if os.path.exists(airshed_path):
#     airshed_ax = plot_airshed(airshed_path)
# else:   print(f"File {airshed_path} not found. Please check the path and try again.")


# def plot_region(path, title='delhi-ncr-Region'):
#     # Load the shapefile using geopandas
#     gdf = gpd.read_file(path)
#     gdf = gdf.to_crs(epsg=32644)  # Ensure the GeoDataFrame is in 

#     # Plot the shapefile
#     fig, ax = plt.subplots(figsize=(10, 10))        
#     gdf.plot(ax=ax, color='lightgreen', alpha=1, edgecolor='black')
#     # Set title and labels
#     ax.set_title(title)
#     ax.set_xlabel('Longitude')
#     ax.set_ylabel('Latitude')
#     # Show the plot
#     plt.show()


def plot_region_with_grid(path, title='Delhi-NCR Region with 60km Grid'):

    # Load and project to UTM (meters)
    gdf = gpd.read_file(path)
    gdf = gdf.to_crs(epsg=32644)

    # Get bounding box
    minx, miny, maxx, maxy = gdf.total_bounds

    # Grid size (60 km)
    grid_size = 60000  # meters

    # Create grid polygons
    grid_cells = []
    for x in np.arange(minx, maxx, grid_size):
        for y in np.arange(miny, maxy, grid_size):
            grid_cells.append(box(x, y, x + grid_size, y + grid_size))

    grid = gpd.GeoDataFrame(geometry=grid_cells, crs=gdf.crs)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, edgecolor='black')
    grid.boundary.plot(ax=ax, color='red', linewidth=1)

    ax.set_title(title)
    ax.set_xlabel("Easting (meters)")
    ax.set_ylabel("Northing (meters)")



    plt.show()


# import matplotlib.pyplot as plt
# import numpy as np
# import geopandas as gpd
# import contextily as cx
# from shapely.geometry import box

# def plot_region_with_grid(path, title='Delhi-NCR Region with 60km Grid'):

#     # Load and project to UTM (meters)
#     gdf = gpd.read_file(path)
#     gdf = gdf.to_crs(epsg=32644)

#     minx, miny, maxx, maxy = gdf.total_bounds
#     grid_size = 60000  # 60 km

#     grid_cells = []
#     for x in np.arange(minx, maxx, grid_size):
#         for y in np.arange(miny, maxy, grid_size):
#             grid_cells.append(box(x, y, x + grid_size, y + grid_size))

#     grid = gpd.GeoDataFrame(geometry=grid_cells, crs=gdf.crs)

#     # Clip grid to region (cleaner visualization)
#     grid = gpd.overlay(grid, gdf, how="intersection")

#     fig, ax = plt.subplots(figsize=(10, 10))

#     # Plot region boundary
#     gdf.plot(ax=ax, edgecolor='black', color='lightblue',  linewidth=2)

#     # Plot grid
#     grid.boundary.plot(ax=ax, color='red', linewidth=1)

#     # Add satellite basemap
#     # cx.add_basemap(ax, source=cx.providers.Esri.WorldImagery, crs=gdf.crs)

#     ax.set_title(title)
#     ax.set_xlabel("Easting (meters)")
#     ax.set_ylabel("Northing (meters)")
#     ax.grid(True)

#     plt.show()

region_path = 'data/raw/delhi_ncr_region.geojson'
if os.path.exists(region_path):
    plot_region_with_grid(region_path)
else:   print(f"File {region_path} not found. Please check the path and try again.")


