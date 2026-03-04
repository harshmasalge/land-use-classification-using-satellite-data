import geopandas as gpd
import os
import time


#Copy png images from rgb folder to two separate folders useful_images and not_useful_images based on image file names


def filter_images(rgb_path= './data/raw/rgb/', region_path = './data/raw/delhi_ncr_region.geojson'):
    inside_images_folder = './data/processed/inside_images/'
    outside_images_folder = './data/processed/outside_images/'

    # Create the folders if they don't exist
    os.makedirs(inside_images_folder, exist_ok=True)
    os.makedirs(outside_images_folder, exist_ok=True)

    gdf = gpd.read_file(region_path)
    region= gpd.GeoDataFrame(gdf, geometry='geometry')

    
    merged_polygon= region.union_all()
    image_paths=os.listdir(rgb_path)
    print(f"Total images to filter: {len(image_paths)}\n")
    print("=================================")
    print("Starting filtering process in 2sec...")
    time.sleep(2)

    # List all files in the rgb folder
    for filename in image_paths:
        if filename.endswith('.png'):
            image_path = os.path.join(rgb_path, filename)
            # Extract the coordinates from the filename
            try:
                lat, lon = map(float, filename[:-4].split('_'))
                point = gpd.points_from_xy([lon], [lat], crs='EPSG:4326')

                # Check if the point is within the region
                if merged_polygon.contains(point):
                    # Move the image to the useful_images folder
                    os.rename(image_path, os.path.join(inside_images_folder, filename))
                    # print(f"Moved {filename} to {inside_images_folder}")
                else:
                    # Move the image to the not_useful_images folder
                    os.rename(image_path, os.path.join(outside_images_folder, filename))
                    # print(f"Moved {filename} to {outside_images_folder}")
            except ValueError:
                print(f"Filename {filename} does not contain valid coordinates. Skipping.")

    print(f"Finished filtering all images.")
    print(f"Total images moved to {inside_images_folder}: {len(os.listdir(inside_images_folder))}")
    print(f"Total images moved to {outside_images_folder}: {len(os.listdir(outside_images_folder))}")


filter_images()