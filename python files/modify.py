import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = input("Input the path of csv file: ")



def convert_backslashes(path):
    converted_path = ''
    for char in path:
        if char == '\\':
            converted_path += '/'
        else:
            converted_path += char
    return converted_path

path = convert_backslashes(path)

df = pd.read_csv(path)
columns_to_delete = ['LABEL', 'POSITION_Z', 'POSITION_T', 'VISIBILITY', 'MANUAL_SPOT_COLOR', 'MEAN_INTENSITY_CH1', 'MEDIAN_INTENSITY_CH1', 'MIN_INTENSITY_CH1', 'MAX_INTENSITY_CH1', 'TOTAL_INTENSITY_CH1', 'STD_INTENSITY_CH1']
df = df.drop(columns=columns_to_delete)
df.rename(columns={'ID': 'cellid'}, inplace=True)
df.to_csv(path, index=False)