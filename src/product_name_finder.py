import pytesseract
from pytesseract import Output
import cv2
import re
import numpy as np
#take image in (hard coded)
img = cv2.imread('week_1_page_1_13.png')
#saturate the image for better clarity
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = ((img.astype(np.float32) - 128.0) * 100.0) + 128.0
img = np.clip(img, 0, 255).astype(np.uint8)

from fuzzywuzzy import fuzz
from products_list import getProductsList
products = getProductsList();

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe';

image_string = pytesseract.image_to_string(img, output_type=Output.DICT)
image_data = pytesseract.image_to_data(img, output_type=Output.DICT)

#print(image_string)
n_boxes = len(image_data['level'])
guess = "";
for i in range(n_boxes):
	if image_data['height'][i] > 37 and image_data['height'][i] < 60 and re.search('[a-zA-Z1-9]', image_data['text'][i]): 
		guess += image_data['text'][i] + " "	

print(guess)

best_ratio = 0
best_idx = 0
i=0

for x in products:
	ratio = fuzz.ratio(guess,x)
	if ratio < best_ratio:
		i+=1
		continue
	best_ratio = ratio
	best_idx = i
	#print(ratio,best_idx,search_str,x)
	i+=1

best_guess = products[best_idx]
confidence = best_ratio
print(products[best_idx])
#TODO: set low threshold for match s.t. no random pictures are used 
# if(best_ratio > 60):
# 	print(best_guess,best_ratio)
	
# 	biggest_text = 0
# 	biggest_index = 0
# 	for i in range(image_data):
# 		if()
# else: