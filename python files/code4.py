import os
import numpy as np
import pandas as pd
from skimage import io
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

def process_tiff_file(tiff_path):
    tiff_image = io.imread(tiff_path)
    min_intensity = np.min(tiff_image)
    return min_intensity

channels = ['CFP', 'YFP']
files = os.listdir(path)
for channel in channels:
    tif_folder_path = path + '/' + channel
    csv_folder_path = tif_folder_path + '/imagej_' + scale

    for tif_filename in tqdm(os.listdir(tif_folder_path)):
        if tif_filename.endswith('.tif'):
            tif_path = os.path.join(tif_folder_path, tif_filename)
            
            # Calculate the least pixel value in the TIFF file
            min_intensity = process_tiff_file(tif_path)
        
            # Find the corresponding CSV file
            csv_filename = os.path.splitext(tif_filename)[0] + '.csv'
            csv_path = os.path.join(csv_folder_path, csv_filename)
            
            if os.path.exists(csv_path):
                # Modify the "mean" column in the CSV file
                df = pd.read_csv(csv_path)
                if "Mean" in df.columns:
                    df["Mean"] = df["Mean"] - min_intensity
                    df.to_csv(csv_path, index=False)




#Rename the column of CFP files

folder_path = path+ '/CFP/imagej_' + scale

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

for csv_file in tqdm(csv_files):
    file_path = os.path.join(folder_path, csv_file)

    # Read the CSV file using pandas
    df = pd.read_csv(file_path)

    # Check if 'mean' column exists and rename it to 'cfp_mean'
    if 'Mean' in df.columns:
        df.rename(columns={'Mean': 'cfp_Mean'}, inplace=True)

        # Save the DataFrame back to the same CSV file
        df.to_csv(file_path, index=False)




folder1_path = path + "/CFP/imagej_" + scale
folder2_path = path + "/YFP/imagej_" + scale

folder1_csv_files = [f for f in os.listdir(folder1_path) if f.endswith(".csv")]
folder2_csv_files = [f for f in os.listdir(folder2_path) if f.endswith(".csv")]

for csv_file in tqdm(folder1_csv_files):

    file1_path = os.path.join(folder1_path, csv_file)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file1_path)
    # List of column names to delete
    columns_to_delete = [' ', 'XM', 'YM', 'Perim.', 'Area']
    # Delete the specified columns
    df = df.drop(columns=columns_to_delete)


    df['serial_no'] = range(1, len(df) + 1)
    df = df[['serial_no'] + [col for col in df.columns if col != 'serial_no']]
    df.to_csv(file1_path, index=False)

for csv_file in folder2_csv_files:
    file2_path = os.path.join(folder2_path, csv_file)
    df = pd.read_csv(file2_path)
    df.rename(columns={" ": "serial_no"}, inplace=True)
    df.to_csv(file2_path, index=False)


# Iterate through the common CSV files (e.g., 1.csv, 2.csv, etc.)
for csv_file in tqdm(folder1_csv_files):
    if csv_file in folder2_csv_files:
        file1_path = os.path.join(folder1_path, csv_file)
        file2_path = os.path.join(folder2_path, csv_file)
        
        # Read both CSV files into DataFrames
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        # Merge based on a common column (e.g., 'common_column_name')
        merged_df = pd.merge(df2, df1[['serial_no', 'cfp_Mean']], on='serial_no', how='left')
        
        # Overwrite the CSV file in the second folder with the merged data
        merged_df.to_csv(file2_path, index=False)


folder =  path + "/YFP/imagej_" + scale
folder_csv_files = [f for f in os.listdir(folder1_path) if f.endswith(".csv")]

for csv_file in tqdm(folder_csv_files):
    file_path = os.path.join(folder, csv_file)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    df['FRET'] = df['Mean'] / df['cfp_Mean']
    df.to_csv(file_path, index=False)


folder2_path = path + "/analysis"

folder2_csv_files = [f for f in os.listdir(folder2_path) if f.endswith(".csv")]

for csv_file in tqdm(folder2_csv_files):
    file2_path = os.path.join(folder2_path, csv_file)
    df = pd.read_csv(file2_path)

    df['serial_no'] = range(1, len(df) + 1)


    df = df[['serial_no'] + [col for col in df.columns if col != 'serial_no']]

    df.to_csv(file2_path, index=False)


# Match ImageJ files with python files
# Define the paths for input folders
input_folder_1 = path + "/YFP/imagej_" + scale
input_folder_2 = path + '/analysis'
# Define the output folder
output_folder = input_folder_1 + '/merged'
os.makedirs(output_folder, exist_ok=True)
# List all CSV files in the first input folder
input_files_1 = [f for f in os.listdir(input_folder_1) if f.endswith('.csv')]

# Process each input CSV file
for input_file in tqdm(input_files_1):
    # Construct the full paths for input files in both folders
    input_csv_path_1 = os.path.join(input_folder_1, input_file)
    input_csv_path_2 = os.path.join(input_folder_2, input_file)
    
    # Read the CSV files from both folders
    data_1 = pd.read_csv(input_csv_path_1)
    data_2 = pd.read_csv(input_csv_path_2)

    # Merge the two DataFrames based on the "serial_no" column
    merged_data = pd.merge(data_1, data_2, on='serial_no', how='left')

    # Save the merged DataFrame to the output folder
    output_csv_path = os.path.join(output_folder, input_file)
    merged_data.to_csv(output_csv_path, index=False)
