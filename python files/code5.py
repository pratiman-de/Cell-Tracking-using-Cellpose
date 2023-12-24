import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from PIL import Image
import cv2
import pandas as pd
from matplotlib import cm
from skimage.io import imread, imsave
from tqdm.auto import tqdm




path = input("Input the path: ")


def convert_backslashes(path):
    converted_path = ''
    for char in path:
        if char == '\\':
            converted_path += '/'
        else:
            converted_path += char
    return converted_path

path = convert_backslashes(path)


while True:
    try:
        scale = input("Input scale factor: ")
        scale2 = int(scale)  # Try to convert the input to an integer
        break  # If successful, exit the loop
    except ValueError:
        print("e.g. 100, 90")

fret_min = float(input("Input FRET min: ")) #0.99
fret_max = float(input("Input FRET max: ")) #1.55
cmap = cm.get_cmap('rainbow') # Color map for FRET values

# Run this code only once if you get "ValueError: cannot convert float NaN to integer" in the next code block
tif_directory = path + '/YFP'
csv_directory = path + '/YFP/imagej_' + scale + '/merged'


for filename in tqdm(os.listdir(csv_directory)):
    if filename.endswith(".csv"):
        # Construct the full file path
        file_path = os.path.join(csv_directory, filename)

        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)

        # Drop rows with any empty cell
        df.dropna(axis=0, how='any', inplace=True)

        # Save the modified DataFrame back to the same CSV file
        df.to_csv(file_path, index=False)


tif_directory = path + '/YFP'
csv_directory = path + '/YFP/imagej_' + scale + '/merged'
output_directory = path + '/YFP/image_' + scale

os.makedirs(output_directory, exist_ok=True)

# Iterate through TIF files in the TIF directory
tif_files = [filename for filename in os.listdir(tif_directory) if filename.endswith('.tif')]

for tif_filename in tqdm(tif_files):
    tif_path = os.path.join(tif_directory, tif_filename)
    csv_filename = tif_filename.replace('.tif', '.csv')
    csv_path = os.path.join(csv_directory, csv_filename)

    if os.path.exists(csv_path):
        # Load the input grayscale TIF image
        input_image = imread(tif_path)
        image_shape = input_image.shape

        # Load CSV file using pandas and extract required columns
        coordinates_df = pd.read_csv(csv_path)
        coordinates = coordinates_df[['XM', 'YM', 'FRET', 'string']].values

        # Create a black background RGB image based on input image dimensions
        rgb_image = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.uint16)

        # Process each coordinate and polygon
        for x, y, fret_value, polygon_str in coordinates:
            x = float(x)
            y = float(y)
            fret_value = float(fret_value)

            # Scale the FRET value to the color map range
            normalized_fret = (fret_value - fret_min) / (fret_max - fret_min)
            fret_color = np.array(cmap(normalized_fret)[:3]) * 65535  # Convert to 16-bit range

            # Parse polygon coordinates from the string
            polygon_coords = list(map(float, polygon_str.strip().split()))

            # Create the x and y lists for the polygon vertices
            x_p = polygon_coords[0::2]
            y_p = polygon_coords[1::2]

            # Add the x and y values to every element of the lists
            x_p = [int(x + value) for value in x_p]
            y_p = [int(y + value) for value in y_p]

            # Convert the vertices to numpy array
            polygon_vertices = np.array(list(zip(x_p, y_p)), dtype=np.int32)

            # Draw the polygon on the RGB image
            cv2.fillPoly(rgb_image, [polygon_vertices], fret_color)

        # Save the modified image in the output directory
        output_image_path = os.path.join(output_directory, f'{tif_filename}')
        imsave(output_image_path, rgb_image)

