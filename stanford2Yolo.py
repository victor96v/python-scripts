#ADAPTATION FROM STANDFORD DATASET TO YOLO
import glob
import cv2
import os.path
from pymediainfo import MediaInfo

def relativeYoloParameters(x,y,w,h,width,height):
	
	x = x/width
	y = y/height
	w = w/width
	h = h/height
	return x,y,w,h


def getCategoryYolo(cat):

	if(cat == "Pedestrian" or cat=="Skater" or "Biker"):
		return 0
	elif(cat=="Bus" or cat=="Car" or cat=="Cart"):
		return 1

def writeNewAnnotLine(line_splitted,width,height):

	new_annot_line_array = []
	for pos in range(1,6):
		line_splitted[pos] = int(line_splitted[pos])

	num_category  = getCategoryYolo(line_splitted[len(line_splitted)-1])
	new_annot_line_array.append(num_category)
	x = int((line_splitted[3]+line_splitted[1])/2)
	y = int((line_splitted[4]+line_splitted[2])/2)
	w = line_splitted[3]-line_splitted[1]
	h = line_splitted[4]-line_splitted[2]
	x,y,w,h = relativeYoloParameters(x,y,w,h,width,height)
	new_annot_line_array.extend([x,y,w,h])
	line_string = (' '.join(map(str,new_annot_line_array)))
	return line_string



if __name__ == "__main__":

	path_root_videos  = "/home/victor/datasets/stanford_campus_dataset/videos"
	path_origin_annot = "/home/victor/datasets/stanford_campus_dataset/annotations"
	path_new_annot    = "/home/victor/datasets/stanford_campus_dataset/train_frames"

	parser = argparse.ArgumentParser(description='Process a video.')
    parser.add_argument('video_origin', metavar='video_path', type=str,
                        help='set origin of videos')
    parser.add_argument('origin_annot', metavar='org_annot', type=str,
                        help='set origin of annotations')

	annot_files = glob.glob(path_origin_annot + '/**/*.txt', recursive=True)

	for file in annot_files:

		file_splitted = file.split('/')
		scene = file_splitted[len(file_splitted)-3]
		video_num = file_splitted[len(file_splitted)-2]
		path_current_video = path_root_videos+'/'+scene+'/'+video_num+'/video.mov'

		vcap = cv2.VideoCapture(path_current_video)
		r,frame = vcap.read()

		width,height = frame.shape[0],frame.shape[1]
		file_dir = scene+'/'+scene+'_'+video_num
		print(path_new_annot+'/'+file_dir+'.txt')

		with open(file,'r') as orig_annot_file_txt:

			for line in orig_annot_file_txt:

				line_splitted = line.split()
				line_string = writeNewAnnotLine(line_splitted,width,height)
				frame = line_splitted[5]
				new_file_path = path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt'

				if(os.path.exists(new_file_path)):
					with open(path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt','a') as new_annot_file_txt:
						new_annot_file_txt.write(line_string+'\n')
						print(path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt')
				else:
					with open(path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt','w') as new_annot_file_txt:
						new_annot_file_txt.write(line_string+'\n')
						print(path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt')

