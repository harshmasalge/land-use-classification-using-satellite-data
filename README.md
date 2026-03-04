# AI Sustainability Project

This project focuses on analyzing and classifying land cover using satellite imagery and computer vision models.

## Dataset

1. Download the dataset from the following link:
   - **[INSERT DATASET LINK HERE]**
2. Extract and place the raw dataset files (e.g., `.tif`, `.geojson`, `.zip`, `rgb/` folder) into the `data/raw/` directory.

## Project Structure

- `data/raw/`: Original downloaded datasets and region boundaries.
- `data/processed/`: Extracted patches, arrays, and train/test splits.
- `models/`: Trained model weights (`.pth`) and encoders (`.pkl`).
- `outputs/`: Generated plots and confusion matrices.
- `scripts/`: Source code for processing and modeling.

## How to Run

Follow these steps in order to process the data, train the model, and evaluate it. Make sure you are running these commands from the root directory of the project.

### 1. Requirements

Install the required Python packages:
```bash
pip install -r requiremants.txt
```

### 2. Data Filtering

Filter the raw RGB images based on the region boundaries to separate useful images for training:
```bash
python scripts/filter.py
```
*(This will populate `data/processed/inside_images/` and `data/processed/outside_images/`)*

### 3. Dataset Preparation

Process the images, extract land cover labels from the raster data, and split them into training and testing sets:
```bash
python scripts/dataset-prep.py
```
*(This generates `.npy` files for features and labels in `data/processed/` and displays a class distribution plot)*

### 4. Model Training

Train the ResNet18 model on the processed dataset:
```bash
python scripts/model_training.py
```
*(The trained model will be saved as `models/resnet18_landuse.pth` and the label encoder as `models/label_encoder.pkl`)*

### 5. Model Evaluation

Evaluate the trained model on the test set and generate a confusion matrix:
```bash
python scripts/model_evaluation.py
```

### 6. Visualizations (Optional)

To plot the regions and grids for visualization:
```bash
python scripts/visualisations.py
```
