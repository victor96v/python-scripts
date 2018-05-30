import os
import cv2
import glob
import argparse

from pathlib import Path


def writeImagesFromVideo(video_path):

	cap = cv2.VideoCapture(video_path)
	counter = 0

	video_path_splitted = video_path.split('/')
	scene = video_path_splitted[len(video_path_splitted)-3]
	video_num = video_path_splitted[len(video_path_splitted)-2]
	scene_dir = str(Path.home())+'/train_frames'
	if not os.path.exists(scene_dir):
    	os.makedirs(scene_dir)
	
	while True:

		r, frame = cap.read()

		if r:
			counter += 1
			if(os.path.exists(scene_dir+'/'+scene+'_'+video_num+'_frame'+str(counter)+'.jpg') == False):
				cv2.imwrite(scene_dir+'/'+scene+'_'+video_num+'_frame'+str(counter)+'.jpg',frame)
				print('imagen '+scene_dir+'/'+scene+'_'+video_num+'_frame'+str(counter)+'.jpg'+' creada')
			else:
				print('imagen ',counter,'de',scene,video_num,' ya obtenida')
				continue
		else:
			break


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process a video.')
    parser.add_argument('video_origin', metavar='video_path', type=str,
                        help='set origin of videos')

    args = parser.parse_args()

	video_files  = glob.glob(args.video_origin + '/**/*.mov', recursive=True)
	for video_path in video_files:
		writeImagesFromVideo(video_path)