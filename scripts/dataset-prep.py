import os
import rasterio
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# Path to raster
landcover_path = "data/raw/worldcover_bbox_delhi_ncr_2021.tif"

# Open raster
try:
    lc = rasterio.open(landcover_path)
    print(f"Successfully opened raster: {landcover_path}")
    print("Raster CRS:", lc.crs)
except Exception as e:
    print(f"Error opening raster: {e}")
    exit(1)


labels = []
image_names = []

rgb_path = "data/processed/inside_images"


# Read the raster and extract labels for each image
try:
    for filename in os.listdir(rgb_path):
        if filename.endswith(".png"):
            
            # Extract lat lon from filename
            lat, lon = map(float, filename[:-4].split("_"))
            
            height = lc.height
            width = lc.width

            row, col = lc.index(lon, lat)

            half = 64

            if (row-half < 0 or row+half > height or
                col-half < 0 or col+half > width):
                continue

            window = rasterio.windows.Window(
                col-half,
                row-half,
                128,
                128
            )

            patch = lc.read(1, window=window)

            if patch.shape == (128, 128):
                labels.append(patch)
                image_names.append(filename)
    # print("try block executed successfully.")

except Exception as e:
    print(f"Error processing images: {e}")
    exit(1)

print(f"Total images processed: {len(image_names)}")


# Get mode class for each patch
try:    
    print("Calculating mode class for each patch...")
    final_labels = []

    for patch in labels:
        values = patch.flatten()
        values = values[values != 0]  # remove no-data

        if len(values) == 0:
            final_labels.append(None)
            continue

        mode_class = Counter(values).most_common(1)[0][0]
        final_labels.append(mode_class)
    print("Mode class calculation completed.")
except Exception as e:
    print(f"Error calculating mode class: {e}")
    exit(1)
# Map ESA classes to simplified categories
esa_mapping = {
    # Built
    50: "Built-up",

    # Agriculture
    40: "Cropland",

    # Water
    80: "Water",

    # Natural Vegetation
    10: "Vegetation",
    20: "Vegetation",
    30: "Vegetation",
    90: "Vegetation",
    95: "Vegetation",

    # Others (rare in Delhi region)
    60: "Others",
    70: "Others",
    100: "Others"
}
simplified_labels = []

for label in final_labels:
    simplified_labels.append(esa_mapping.get(label, "Others"))
print("Simplified Label mapping completed.")



#Train-test split
X = image_names
y = simplified_labels

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.4,
        random_state=42,
        stratify=y
    )
    np.save("data/processed/X_train.npy", X_train)
    np.save("data/processed/X_test.npy", X_test)
    np.save("data/processed/y_train.npy", y_train)
    np.save("data/processed/y_test.npy", y_test)
    print("Train-test split successfully saved to numpy files.")
except Exception as e:
    print(f"Error during train-test split: {e}")
    exit(1)


#Class distribution

train_counts = pd.Series(y_train).value_counts()
test_counts = pd.Series(y_test).value_counts()

plt.figure(figsize=(12,5))

#Train Plot
ax1 = plt.subplot(1, 2, 1)
train_counts.plot(kind='bar', ax=ax1)

ax1.set_title("Train Class Distribution")
ax1.set_ylabel("Count")

for i, value in enumerate(train_counts):
    ax1.text(i, value, str(value),
             ha='center', va='bottom')


#Test Plot
ax2 = plt.subplot(1, 2, 2)
test_counts.plot(kind='bar', ax=ax2)

ax2.set_title("Test Class Distribution")
ax2.set_ylabel("Count")

for i, value in enumerate(test_counts):
    ax2.text(i, value, str(value),
             ha='center', va='bottom')

plt.tight_layout()
plt.show()