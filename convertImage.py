import os
import sys
import cv2
import numpy as np
import rawpy
import imageio

path = 'Data\\raw_images'

def usingRawpy(file_path):
	raw = rawpy.imread(file_path)
	rgb = raw.postprocess()
	imageio.imsave('test.jpeg', rgb)

	# try:
	# except Exception as e:
	# 	print(e)
	for file in os.listdir():
		if file.endswith(".raw"):
			raw = rawpy.imread(f'{path}\{file}')
			thumb = raw.extract_thumb()
			time.sleep(1)

def grayscale(file_path):
	fd = open(file_path)
	rows = 1080
	cols = 1440
	f = np.fromfile(fd, dtype=np.uint8,count=rows*cols)
	im = f.reshape((rows, cols)) #notice row, column format
	fd.close()

	cv2.imshow('Test Drive', im)
	# 17 ms = 60 fps
	cv2.waitKey(16)
	# cv2.destroyAllWindows()

# os.chdir(path)
# print("Path:", os.getcwd())
# for file in os.listdir():
# 	if file.endswith(".raw"):
# 		print(f'{os.getcwd()}\{file}')
# 		grayscale(f'{os.getcwd()}\{file}')

# cv2.destroyAllWindows()