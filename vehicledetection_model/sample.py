import os
import matplotlib.pyplot as plot
import logging
import argparse
import scipy.io
import scipy.misc
import numpy as np
import pandas as pd
import PIL
import tensorflow as tf
import re
import time
import os.path
import cv2
import pathlib
from time import sleep
from keras import backend as K
from keras.layers import Input, Lambda, Conv2D
from keras.models import load_model, Model
from yolo_utils import read_classes, read_anchors, generate_colors, preprocess_image, draw_boxes, scale_boxes
from yad2k.models.keras_yolo import yolo_head, yolo_boxes_to_corners, preprocess_true_boxes, yolo_loss, yolo_body, yolo_eval
from imageresize import image_resize, delete_resize_image

#Create and configure logger
logging.basicConfig(filename="detectiondata.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sess = K.get_session()

class_names = read_classes("model_data/coco_classes.txt")
anchors = read_anchors("model_data/yolo_anchors.txt")

# ===================== very important please specify===================================
image_shape = (800., 850.)

yolo_model = load_model("model_data/yolo.h5")

#yolo_model.summary()

yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))

scores, boxes, classes = yolo_eval(yolo_outputs, image_shape)



def predict(sess, image_file,option,count):
	"""
	Runs the graph stored in "sess" to predict boxes for "image_file". Prints and plots the preditions.

	Arguments:
	sess -- your tensorflow/Keras session containing the YOLO graph
	image_file -- name of an image stored in the "images" folder.

	Returns:
	out_scores -- tensor of shape (None, ), scores of the predicted boxes
	out_boxes -- tensor of shape (None, 4), coordinates of the predicted boxes
	out_classes -- tensor of shape (None, ), class index of the predicted boxes

	Note: "None" actually represents the number of predicted boxes, it varies between 0 and max_boxes.
	"""
	logger.info(str(image_file))
	# Preprocess your image
	if option == 1:
		image, image_data = preprocess_image("images/" + image_file, model_image_size = (608, 608))
	else:
		image, image_data = preprocess_image("incoming_from_haar/" + image_file, model_image_size = (608, 608))
	# Run the session with the correct tensors and choose the correct placeholders in the feed_dict.
	# You'll need to use feed_dict={yolo_model.input: ... , K.learning_phase(): 0})
	out_scores, out_boxes, out_classes = sess.run([scores,boxes,classes],feed_dict={yolo_model.input:image_data,K.learning_phase():0})
	# print(out_classes,"HELLOOO")
	# input("press enter")
	x=0
	y=0
	print(out_classes)
	if [2] in out_classes:
		# input("entererer")
		image.save(os.path.join("out", str(count)+".jpg"), quality=90)
		print("car found")
		count+=1
	# # Print predictions info
	# print('Found {} boxes for {}'.format(len(out_boxes), image_file))
	# # Generate colors for drawing bounding boxes.
		
		# colors = generate_colors(class_names)
		# # Draw bounding boxes on the image file
		# x,y=draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors,logger)
		# # Save the predicted bounding box on the image
		# image.save(os.path.join("out", image_file), quality=90)
		# print(x,y)
		
		
	# # Display the results in the notebook
	# output_image = scipy.misc.imread(os.path.join("out", image_file))


	# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
	# cv2.imshow('image',output_image)
	# cv2.waitKey(0)
	# logger.info(str(image_file)+'\t'+str(pclass)+'\t'+str(pscore)+'\t'+str(out_boxes))
	return out_scores, out_boxes, out_classes,count,x,y

option = 1 	# 1 for reading all the available frames at once and running yolo on it
			# 2 for reading incoming frame from HAAR and runing yolo

# option = int(input("1. process all at once (images present in \\images\\ dir)\n2. process incoming from haar (images present in \\incoming_from_haar\\ dir)\ninput: "))
option=1
logger.info("OPTION CHOSEN: "+str(option))
X1=[]
Y2=[]
X2=[]
Y1=[]
i=0
if option == 1:
	count=0
	while True:
		i+=5
		# i+=1
		if not os.path.exists('images\\'+str(i)+".jpg"):
			time.sleep(5)
			print("\n\nwaiting\n\n")
			i-=5
			continue
		# if i>=104 and i<162:
		# 	#starts here

		# if os.path.isfile('images\\'+str(i)+".jpg") == False:
		# 	break
		# image_resize(""+str(i)+".jpg",option)

		out_scores, out_boxes, out_classes,count,x,y = predict(sess, ""+str(i)+".jpg",option,count)
		# 	plot.plot(x,y,'go--', linewidth=2, markersize=2)
		# 	X1.append(x)
		# 	Y1.append(y)
		# elif i==162:
		# 	print(len(X1),len(Y1))
		# 	plot.plot(np.unique(X1), np.poly1d(np.polyfit(X1, Y1, 1))(np.unique(X1)))
		# 	# plot.show()
		# elif i>470 and i<505:
		# 	out_scores, out_boxes, out_classes,count,x,y = predict(sess, ""+str(i)+".jpg",option,count)
		# 	plot.plot(x,y,'ro--', linewidth=2, markersize=2)
		# 	X2.append(x)
		# 	Y2.append(y)
		# elif i==505:
		# 	print(len(X2),len(Y2))
		# 	plot.plot(np.unique(X2), np.poly1d(np.polyfit(X2, Y2, 1))(np.unique(X2)))
		# 	plot.show()
		# else:
		# 	out_scores, out_boxes, out_classes,count,x,y = predict(sess, ""+str(i)+".jpg",option,count)
		delete_resize_image(""+str(i)+".jpg",option)
		print('classes: ', out_classes," i=",i)
elif option == 2:
	while True:
		images = os.listdir('incoming_from_haar/')
		if len(images) != 0:
			for img in images:
				image_resize(img,option)
				out_scores, out_boxes, out_classes = predict(sess, img,option)
				delete_resize_image(img,option)
				# print('clases: ', out_classes)
				# print(out_boxes[1][1],"hello")
		else:
			pass
		# print('looping')
else:
	print('wrong input')
