import xml.etree.ElementTree as ET
import re
import numpy as np
import pandas as pd
import os
from tqdm.auto import tqdm




print("Rename the FRET xml file as YFP.xml")
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

file_path = path + '/' + 'YFP.xml'
output_path = path + '/' + 'analysis'




def find_line_numbers_with_term(xml_file, term):
    line_numbers = []
    
    with open(xml_file, 'r') as f:
        lines = f.readlines()
    
    for line_number, line in enumerate(lines, start=1):
        if term in line:
            line_numbers.append(line_number)
    
    return line_numbers

def remove_until_char_found(input_str, target_char):
    index = input_str.find(target_char)
    if index != -1:
        removed_chars = input_str[:index + 1]
        remaining_str = input_str[index + 1:]
    else:
        removed_chars = ""
        remaining_str = input_str
    
    return removed_chars, remaining_str

def remove_from_back_until_char_found(input_str, target_char):
    index = input_str.rfind(target_char)
    if index != -1:
        removed_chars = input_str[index:]
        remaining_str = input_str[:index]
    else:
        removed_chars = ""
        remaining_str = input_str
    return removed_chars, remaining_str





os.makedirs(output_path, exist_ok=True)
tree = ET.parse(file_path)
root = tree.getroot()
a = find_line_numbers_with_term(file_path,"<SpotsInFrame frame")
b = find_line_numbers_with_term(file_path,"</SpotsInFrame>")
j = 1
cellid_list, pos_x_list, pos_y_list, stri = [], [], [], []


with open(file_path, 'r') as file:
    lines = file.read().split('\n')


for i in tqdm(range(a[0], b[len(b)-1])):

    data = {"pos_x": pos_x_list, "pos_y": pos_y_list, "string": stri, "cellid": cellid_list}
    if len(lines[i]) <50:        
        if len(lines[i]) < 24:
            df = pd.DataFrame(data)
            file_name = str(j) + '.csv'
            df.to_csv(output_path + '/' + file_name, index=False)
            j = j + 1
            cellid_list, pos_x_list, pos_y_list, mean_intensity_list, median_intensity_list, total_intensity_list, stri = [], [], [], [], [], [], []
 
            i = i + 1
        else:
            i = i + 1
    else:
        first, edit = remove_until_char_found(lines[i], '>') #it's editing the line_no i.e. the remaining string
        end, number_st = remove_from_back_until_char_found(edit, '</')               
        stri.append(number_st)
        first, z = remove_until_char_found(first, '"')
       
        first, z = remove_until_char_found(z, '"')

        cellid = first.replace('"', '')
        z, pos_x = remove_until_char_found(z, 'POSITION_X=')
        
        z, pos_x = remove_until_char_found(pos_x, '"')
        pos_x, z = remove_until_char_found(pos_x, '"')
        
        pos_x = pos_x.replace('"', '')
        
        z, pos_y = remove_until_char_found(z, '"')
        
        pos_y, z = remove_until_char_found(pos_y, '"')
        pos_y = pos_y.replace('"', '')
        cellid_list.append(cellid)
        pos_x_list.append(pos_x)
        pos_y_list.append(pos_y) 
        i = i + 1       


print("Done!")