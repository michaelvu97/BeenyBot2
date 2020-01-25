import pytesseract
#from PIL import Image
import numpy as np
import cv2
from pytesseract import Output
import os
from argparse import ArgumentParser

def create_boxes_from_jpg(dir_path: str):

	#Files = a list of filenames in the current directory
	files = os.listdir(dir_path)

	#Manually remove hidden files (.DS_Store) from the filelist
	#Don't use glob to remove hidden files;
	files_no_hidden = []
	for filename in files:
		if not filename.startswith('.'):
			files_no_hidden.append(filename)

   #Go through all the files in the folder
	for filename in files_no_hidden:
		name = os.path.splitext(filename)[0]

		file_path = os.path.join(dir_path, filename)

		new_folder_path =  os.path.join(dir_path, (name + "_boxes"))
		os.mkdir(new_folder_path)
		img_save_string = os.path.join(new_folder_path, name)            

		#file = Image.open(file_name)
		img = cv2.imread(file_path)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Saturate in order to include non-black text in bounding box consideration
		gray = ((gray.astype(np.float32) - 128.0) * 10.0) + 128.0
		gray = np.clip(gray, 0, 255).astype(np.uint8)

		#Blur to create zones to be bounded by cv2
		blur = cv2.GaussianBlur(gray, (9,9), 0)
		thresh = cv2.adaptiveThreshold(blur,40,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,4,30)

		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
		dilate = cv2.dilate(thresh, kernel, iterations=4)

		cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if len(cnts) == 2 else cnts[1]

		ROI_number = 0
		for c in cnts:
			area = cv2.contourArea(c)
			if area > 10000:
				x,y,w,h = cv2.boundingRect(c)
				ROI = img[y:y+h, x:x+w]
				cv2.imwrite((img_save_string + '_{}.png').format(ROI_number), ROI)
				ROI_number += 1

		cv2.imwrite("thresh.jpg", thresh)
		cv2.imwrite("gary.jpg", gray)
		cv2.imwrite("dilate.jpg", dilate)
		cv2.imwrite("img.jpg", img)
		cv2.waitKey()

if __name__ == "__main__":
	parser = ArgumentParser(description='Create box jpgs from an an input directory of files')
	parser.add_argument('--input_directory', type=str, help='filepath to dir')

	args = parser.parse_args()

	create_boxes_from_jpg(args.input_directory)
	#Bounding box estimates 