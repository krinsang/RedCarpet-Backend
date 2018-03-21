import csv
import os
import sys
import copy
import random
import pandas as pd
import numpy as np
from PIL import Image

attr = pd.read_csv("./data.csv")
bbox = pd.read_csv("./list_bbox.csv")
count = 1
length = 276253
for filename in attr['image_name']:
	row = bbox[bbox['image_name'].str.match(filename)]

	x1 = int(row['x_1'])
	x2 = int(row['x_2'])
	y1 = int(row['y_1'])
	y2 = int(row['y_2'])

	image = Image.open(filename)
	image = image.crop(box=(x1, y1, x2, y2))
	image = image.resize((224, 224), Image.BICUBIC)
	image.save(filename)
	print("%d / %d", (count, length))
	count += 1