import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from PIL import Image
import cv2
from matplotlib import cm
from skimage.io import imread, imsave
from tqdm.auto import tqdm
from scipy.spatial import Voronoi, voronoi_plot_2d
from skimage import img_as_ubyte, io

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


tif_directory = path + '/YFP'
csv_directory = path + '/YFP/imagej_' + scale + '/merged'
output_directory = path + '/YFP/voronoi_' + scale
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

        x = coordinates_df['XM'].values
        y = coordinates_df['YM'].values
                
        # Create a list of points with the shifted coordinates
        points = np.column_stack((x, y))

        # Create a Voronoi object
        vor = Voronoi(points)

        # Create a black background RGB image based on input image dimensions
        rgb_image = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.uint16)

        # Plot the Voronoi diagram on the RGB image
        fig, ax = plt.subplots(figsize=(image_shape[1]/100, image_shape[0]/100), dpi=100)
        voronoi_plot_2d(vor, show_vertices=False, ax=ax)
        ax.set_xlim([0, image_shape[1]])
        ax.set_ylim([0, image_shape[0]])

        # Convert the plot to an RGB image with the same dimensions
        plt.tight_layout()
        plt.subplots_adjust(0, 0, 1, 1)
        fig.canvas.draw()

        # Convert the plot to an RGB image and scale it to uint16
        plt_image = np.array(fig.canvas.renderer.buffer_rgba())[:, :, :-1]
        rgb_image = img_as_ubyte(plt_image)

        output_image_path = os.path.join(output_directory, f'frame_{tif_filename}')
        imsave(output_image_path, rgb_image)
        # Close the plot
        plt.close()

