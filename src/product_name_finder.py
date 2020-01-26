import pytesseract
from pytesseract import Output
import cv2
import re
import numpy as np
import os
from fuzzywuzzy import fuzz
from products_list import getProductsList
from units_list import getUnitsList
from promo_parser import parsePromo
from ad_block_data import AdBlockData
from output_to_csv import outputToCsv

#Files = a list of filenames in the current directory
files = os.listdir("..\\..\\..\\flyer_splitter\\flyer_subimages\\week_1_page_3_boxes\\")
products = getProductsList();
units = getUnitsList();

results = []

#Manually remove hidden files (.DS_Store) from the filelist
#Don't use glob to remove hidden files;



flyer_folder_names = os.listdir("..\\..\\..\\flyer_splitter\\flyer_subimages")

for flyer_folder_name in flyer_folder_names:

	flyer_name = flyer_folder_name[:flyer_folder_name.find("_box")]

	print(flyer_name)

	files = os.listdir("..\\..\\..\\flyer_splitter\\flyer_subimages\\" + flyer_folder_name + "\\")
	files_no_hidden = []
	for filename in files:
		if not filename.startswith('.'):
			files_no_hidden.append(filename)

	for filename in files_no_hidden:
		print(flyer_folder_name + "\\" + filename)
		#saturate the image for better clarity
		img = cv2.imread("..\\..\\..\\flyer_splitter\\flyer_subimages\\" + flyer_folder_name + "\\" + filename)
		#print("\nfile is: " + filename)

		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = ((img.astype(np.float32) - 128.0) * 100.0) + 128.0
		img = np.clip(img, 0, 255).astype(np.uint8)

		
		
		pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe';

		image_string = pytesseract.image_to_string(img, config='--psm 4',output_type=Output.DICT)
		image_data = pytesseract.image_to_data(img, config='--psm 4', output_type=Output.DICT)

		#print(image_string)
		guess = "";
		for i in range(len(image_data['text'])):
			if image_data['height'][i] > 40 and image_data['height'][i] < 60 and re.search('[a-zA-Z1-9]', image_data['text'][i]): 
				guess += image_data['text'][i] + " "	

		if re.search("RECEIVE AN EXTRA",guess):
			remove_index = guess.find("RECEIVE AN EXTRA")
			#print("here!",remove_index)
			guess = guess[:remove_index]

		#print("guess is: " + guess)
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
		all_match  = 1
		for i in guess.split(" "):
			if products[best_idx].find != -1:
				confidence+=5
			else:
				all_match=0

		if all_match:
			confidence+=15

		#print(products[best_idx])
		#print(image_string)
		#TODO: set low threshold for match s.t. no random pictures are used 
		if(best_ratio > 60):
			#print(best_guess,best_ratio)	
			biggest_text = 0
			biggest_index = 0
			big_text = ""
			for i in range(len(image_data['text'])):
				if image_data['height'][i] > biggest_text and re.search('[a-zA-Z1-9]', image_data['text'][i]):
					biggest_text = image_data['height'][i]
					biggest_index = i
					big_text = image_data['text'][i]

			split_string = image_string['text'].split("\n")
			big_text_line = ""
			for x in split_string:
				if x.find(big_text) != -1:
					big_text_line = x

			big_text_line = re.sub('7o', '%', big_text_line)

			if products[best_idx].find("Salad") != -1 and big_text_line.find("Sales Valid") != -1:
				continue

			print("biggest text for " + products[best_idx] + " is " + big_text_line)

			organic = 0
			if image_string['text'].find("organic") != -1 or image_string['text'].find("Organic") != -1 or image_string['text'].find("ORGANIC") != -1:
				organic = 1
			else:
				organic = 0

			unit = ""
			if image_string['text'].find('/lb') != -1 or image_string['text'].find('/Ib') != -1:
				unit = "lb"
			elif re.search('[0-9] [Oo][Zz]',image_string['text']):
				unit = "oz"
			else:
				for i in units:
					if image_string['text'].find(i) != -1:
						unit = i

			block_data = AdBlockData()
			block_data.product_name = products[best_idx]
			block_data.flyer_name = flyer_name # UPDATE ABOVE
			block_data.uom = unit
			if organic == 1:
				block_data.organic = True
			block_data.confidence = confidence
			result = parsePromo(big_text_line,image_string['text'])
			if result is not None:
				block_data.least_unit_for_promo = result[0]
				block_data.discount = result[1]
				block_data.unit_promo_price = result[2]
				block_data.save_per_unit = result[3]

			allowedToInsert = True
			for i in range(len(results)):
				if results[i].flyer_name != flyer_name or results[i].product_name != block_data.product_name:
					continue

				if results[i].confidence < confidence:
					print("Overwrote a result")
					del results[i]
				else:
					allowedToInsert = False
				break

			if allowedToInsert:
				results.append(block_data)

outputToCsv(results)

