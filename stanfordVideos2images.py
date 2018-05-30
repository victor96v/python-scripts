import os
import cv2
import glob

video_origin = '/home/victor/datasets/stanford_campus_dataset/videos'

def writeImagesFromVideo(video_path):

	cap = cv2.VideoCapture(video_path)
	counter = 0

	video_path_splitted = video_path.split('/')
	scene = video_path_splitted[len(video_path_splitted)-3]
	video_num = video_path_splitted[len(video_path_splitted)-2]
	scene_dir = video_origin+'/'+scene
	

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

	video_files  = glob.glob(video_origin + '/**/*.mov', recursive=True)
	for video_path in video_files:
		writeImagesFromVideo(video_path)