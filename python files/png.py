import os
from tqdm.auto import tqdm
from PIL import Image

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



# Set the directory path where you want to save PNG images
output_path = path + "/png"
os.makedirs(output_path, exist_ok=True)
print('Output path: ', output_path)
# Get a list of all TIFF files in the input directory
tiff_files = [f for f in os.listdir(path) if f.lower().endswith('.tif')]

# Loop through the TIFF files and convert each to PNG
for tiff_file in tqdm(tiff_files):
    tiff_path = os.path.join(path, tiff_file)
    img = Image.open(tiff_path)
    
    # Extract the image name (without extension) for PNG file naming
    image_name = os.path.splitext(tiff_file)[0]
    
    # Save the image as PNG
    png_path = os.path.join(output_path, image_name + ".png")
    img.save(png_path, format="PNG")    
    img.close()

