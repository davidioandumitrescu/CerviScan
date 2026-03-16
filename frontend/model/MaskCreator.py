import os
import cv2
import numpy as np
import pandas as pd
import csv
from collections import defaultdict
import json


def create_mask(image_shape, circle_coordinates):
    mask = np.zeros(image_shape, dtype=np.uint8)
    for coord in circle_coordinates:
        center = (int(coord['cx']), int(coord['cy']))
        rx= 0 if coord['rx'] is None else coord['rx']
        ry = 0 if coord['ry'] is None else coord['ry']
        r = 0 if coord['r'] is None else coord['r']
        radius = max(int(rx), int(ry),int(r))
        if radius > 0 :
            cv2.circle(mask, center, radius, color=1, thickness=-1)  # Fill the circle
    return mask


def load_annotations_and_create_masks(csv_file, image_shape=(772, 772)):
    # Initialize a dictionary to group data by the first field
    grouped_data = defaultdict(list)

    # Read CSV data from a file
    with open(csv_file, 'r') as file:
        csv_data = file.readlines()

    # Parse and group the data
    for row in csv.reader(csv_data):
        key = row[0]  # The first field is the key
        if len(row) > 5 and row[5]:  # Check if the 6th column (shape details) is present
            try:
                shape_details = json.loads(row[5].replace('""', '"'))
                cx = shape_details.get('cx')
                cy = shape_details.get('cy')
                r = shape_details.get('r')
                rx=shape_details.get('rx')
                ry=shape_details.get('ry')
                if cx is not None and cy is not None and (r is not None or (rx is not None and ry is not None ) ):
                    grouped_data[key].append({'cx': cx, 'cy': cy, 'r': r, 'rx' : rx, 'ry': ry})
                else :
                    grouped_data[key].append({'cx':0, 'cy': 0, 'r':0 , 'rx':0 , 'ry':0})
            except json.JSONDecodeError:
                continue


    imagewithMask=defaultdict(list)
    for image_name,coordinates in grouped_data.items():
        mask = create_mask(image_shape,coordinates)
        imagewithMask[image_name]=mask

    return imagewithMask


# Funcția principală
if __name__ == "__main__":
    file_path='Borcan Valentina_csv T2.csv'
    image_shape=(512,512)
    masks=load_annotations_and_create_masks(file_path,image_shape)

