import numpy as np
import cv2


class BackGroundSubtractor:
	# When constructing background subtractor, we
	# take in two arguments:
	# 1) alpha: The background learning factor, its value should
	# be between 0 and 1. The higher the value, the more quickly
	# your program learns the changes in the background. Therefore, 
	# for a static background use a lower value, like 0.001. But if 
	# your background has moving trees and stuff, use a higher value,
	# maybe start with 0.01.
	# 2) firstFrame: This is the first frame from the video/webcam.
	def __init__(self,alpha,firstFrame):
		self.alpha  = alpha
		self.backGroundModel = firstFrame

	def getForeground(self,frame):
		# apply the background averaging formula:
		# NEW_BACKGROUND = CURRENT_FRAME * ALPHA + OLD_BACKGROUND * (1 - APLHA)
		self.backGroundModel =  frame * self.alpha + self.backGroundModel * (1 - self.alpha)

		# after the previous operation, the dtype of
		# self.backGroundModel will be changed to a float type
		# therefore we do not pass it to cv2.absdiff directly,
		# instead we acquire a copy of it in the uint8 dtype
		# and pass that to absdiff.

		return cv2.absdiff(self.backGroundModel.astype(np.uint8),frame)

cam1 = cv2.VideoCapture('/home/victor/Vídeos/Visiona/PruebasMontegancedo/DJI_0001.MOV')
cam2 = cv2.VideoCapture('/home/victor/Vídeos/Visiona/PruebasMontegancedo/DJI_0002.MOV')

cv2.namedWindow('input1',cv2.WINDOW_NORMAL)
cv2.namedWindow('input2',cv2.WINDOW_NORMAL)

cv2.namedWindow('diff',cv2.WINDOW_NORMAL)
# Just a simple function to perform
# some filtering before any further processing.
def denoise(frame):

    frame = cv2.medianBlur(frame,5)
    frame = cv2.GaussianBlur(frame,(5,5),0)
    
    return frame

ret1,frame1 = cam1.read()
ret2,frame2 = cam2.read()

if ret1 is True:
	backSubtractor = BackGroundSubtractor(0.01,denoise(frame1))
	run = True
else:
	run = False

counter = 0

while(run):
	# Read a frame from the camera
	ret1,frame1 = cam1.read()
	ret2,frame2 = cam2.read()
	counter += 1

	# If the frame was properly read.
	if ret1 is True and ret2 is True:
		# Show the filtered image
		cv2.imshow('input1',denoise(frame1))
		cv2.imshow('input2',denoise(frame2))
		gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
		gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
		diff = abs(gray2-gray1)
		median = cv2.medianBlur(diff,7)
		median[np.where(median >= [180])] = [0]
		median[np.where(median <= [80])]  = [0]
		median2 = cv2.medianBlur(median,7)
		# get the foreground
		foreGround = backSubtractor.getForeground(denoise(frame2))

		# Apply thresholding on the background and display the resulting mask
		ret1, mask = cv2.threshold(foreGround, 15, 255, cv2.THRESH_BINARY)

		# Note: The mask is displayed as a RGB image, you can
		# display a grayscale image by converting 'foreGround' to
		# a grayscale before applying the threshold.
		# cv2.namedWindow('mask',cv2.WINDOW_NORMAL)
		# cv2.imshow('mask',mask)
		cv2.imshow('diff',median2)

		key = cv2.waitKey(10) & 0xFF
	else:
		break

	if key == 27:
		break

cam.release()
cv2.destroyAllWindows()