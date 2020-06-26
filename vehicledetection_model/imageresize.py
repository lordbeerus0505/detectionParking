import cv2
import os
import time

def image_resize(img,opt):
	if opt == 1:
		image = cv2.imread('images/'+str(img))
		image=imutils.resize(image,700)
		image = cv2.copyMakeBorder( image, 150, 150, 100, 100,cv2.BORDER_CONSTANT)
		cv2.imwrite('images/p'+str(img),image)
	else:
		image = cv2.imread('incoming_from_haar/'+str(img))
		image = cv2.copyMakeBorder( image, 150, 150, 100, 100,cv2.BORDER_CONSTANT)
		cv2.imwrite('incoming_from_haar/'+str(img),image)


def delete_resize_image(img,opt):
	if opt==1:
		try:
			os.remove('images/p'+str(img))
		except:
			pass
	else:
		try:
			os.remove('incoming_from_haar/'+str(img))
		except:
			pass
# image_resize('frame30.jpg')
#
# delete_resize_image('frame30.jpg')
# print(os.listdir('incoming_from_haar'))
