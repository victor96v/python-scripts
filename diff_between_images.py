import argparse
import cv2

from skimage.measure import compare_ssim

if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("-f","--first",  required=True, help="first input image")
	ap.add_argument("-s","--second", required=True, help="second")
	args = vars(ap.parse_args())

	img1 = cv2.imread(args["first"])
	img2 = cv2.imread(args["second"])

	gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

	diff_gray  = abs(gray1-gray2)
	diff_img   = abs(img1-img2)

	cv2.namedWindow("diff", cv2.WINDOW_NORMAL)
	cv2.imshow("diff", diff_gray)
	cv2.waitKey(0)