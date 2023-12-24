import os
import shutil
import re

path = input("Input the path: ")
channels = ['CFP', 'YFP']




def convert_backslashes(path):
    converted_path = ''
    for char in path:
        if char == '\\':
            converted_path += '/'
        else:
            converted_path += char
    return converted_path


path = convert_backslashes(path)


def extract_integer(filename):
    match = re.search(r'\d+', filename)
    if match:
        return match.group()
    else:
        return filename

def generate_new_filename(folder_path, filename):
    base_name, extension = os.path.splitext(filename)
    integer_part = extract_integer(base_name)
    
    integer_part = str(int(integer_part))  # Convert to integer to remove leading zeros
    new_filename = f"{integer_part}{extension}"
    
    counter = 1
    while os.path.exists(os.path.join(folder_path, new_filename)):
        new_filename = f"{integer_part}_{counter}{extension}"
        counter += 1
        
    return new_filename

def rename_tif_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.tif'):
            old_name = os.path.join(folder_path, filename)
            new_name = os.path.join(folder_path, generate_new_filename(folder_path, filename))
            os.rename(old_name, new_name)

# Rename the images and move them to respective files

files = os.listdir(path)
for channel in channels:
    extension = channel + ".tif"

    destination_folder = path + '/' + channel
    os.makedirs(destination_folder, exist_ok=True)

    # Move files ending with cfp.tif and yfp.tif to the destination folder
    for file in files:
        if file.endswith(extension):
            source_path = os.path.join(path, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.move(source_path, destination_path)
            #print(f"Moved {file} to {destination_folder}")
    rename_tif_files(destination_folder)


# Delete the other files
try:
    # List all files in the folder
    files = os.listdir(path)
    
    # Iterate through the list of files and delete each one
    for file_name in files:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            #print(f"Deleted: {file_path}")
    
    print("Done!")
except OSError as e:
    print(f"Error deleting files in the folder: {e}")