########################################################################################################
#
# Author: Hyeon Woo Ryou
# Last updated: 02/17/2018
# 
########################################################################################################

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
checking_stuff=0

#Range of colors in RGB
lower_green = np.array([65,80,80])
upper_green = np.array([100,255,255])

lower_blue = np.array([90,80,80])
upper_blue = np.array([130,255,255])

#Store the colors able to detect.
#To add more colors to detect, add variables as shown above
#and add it to these arrays.
lower_colors=[lower_blue,lower_green]
upper_colors=[upper_blue,upper_green]

while(1):
	#Create the screen showing the vision through camera
	_,frame = cap.read()
	frame = cv2.blur(frame,(3,3))
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
	current_lower=lower_colors[checking_stuff]
	current_upper=upper_colors[checking_stuff]
	thresh = cv2.inRange(hsv,current_lower, current_upper)
	thresh2 = thresh.copy()
	
	_,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	
	color_detected = False
	#Minimum size of the color to be detected to perform action
	max_area = 5000
	#Location of upper left side of the image
	image_left = 0
	#For loop to check if color looking for is detected
	for cnt in contours:
		area = cv2.contourArea(cnt)
		#If the color detected is too small, it will disregard it to minimize the error
		if area > max_area:
			x,y,w,h = cv2.boundingRect(cnt)
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
			image_left = x
			perform_action = True
			color_detected = True
		
	if color_detected == False:
		perform_action = False
	
	cv2.imshow('frame',frame)
	cv2.imshow('thresh',thresh2)
	
	#If color is being detected, perform specific actions.
	#To change the action to be performed, edit each blocks.
	#If more colors are added, add more else if statements with appropriate checking_stuff condition.
	if perform_action == True and checking_stuff == 0:
		if (image_left > 400):
			print("right yes")
		elif (image_left < 4):
			print("left yes")
	elif perform_action == True and checking_stuff == 1:
		print("Detecting color at: " + str(image_left))
		print("Size of the detected object with this color is: " + str(area))

	#If 'escape' key is pressed, exit the loop, which will quit the application
	if cv2.waitKey(33)== 27:
		break
	#If 'q' key is pressed, start detecting next color in lower_colors and upper_colors.
	elif(cv2.waitKey(33)==ord('q')):
		if (checking_stuff+1)<len(lower_colors):
			checking_stuff+=1
		else:
			checking_stuff=0
	else:
		continue