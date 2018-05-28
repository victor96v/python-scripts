#ADAPTATION FROM STANDFORD DATASET TO YOLO
import glob
import cv2
import os.path

#GLOBAL VARIABLES

path_origin_annot = "/home/victor/datasets/stanford_campus_dataset/annotations"
path_new_annot    = "/home/victor/datasets/stanford_campus_dataset/custom_annotations"

annot_files = glob.glob(path_origin_annot + '/**/*.txt', recursive=True)

def getCategoryYolo(cat):
	if(cat == "Pedestrian" or cat=="Skater" or "Biker"):
		return 0
	elif(cat=="Bus" or cat=="Car" or cat=="Cart"):
		return 1

if __name__ == "__main__":

	for file in annot_files:

		file_splitted = file.split('/')
		file_dir = file_splitted[len(file_splitted)-3]+'/'+file_splitted[len(file_splitted)-3]+'_'+file_splitted[len(file_splitted)-2]
		print(path_new_annot+'/'+file_dir+'.txt')
		with open(file,'r') as orig_annot_file_txt:
			for line in orig_annot_file_txt:
				new_annot_line_array = []
				line_splitted = line.split()
				for pos in range(1,6):
					line_splitted[pos] = int(line_splitted[pos])
				num_category  = getCategoryYolo(line_splitted[len(line_splitted)-1])
				new_annot_line_array.append(num_category)
				x = int((line_splitted[3]+line_splitted[1])/2)
				y = int((line_splitted[4]+line_splitted[2])/2)
				w = line_splitted[3]-line_splitted[1]
				h = line_splitted[4]-line_splitted[2]
				new_annot_line_array.extend([x,y,w,h])
				line_string = (' '.join(map(str,new_annot_line_array)))
				frame = line_splitted[5]
				new_file_path = path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt'
				if(os.path.exists(new_file_path)):
					with open(path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt','a') as new_annot_file_txt:
						new_annot_file_txt.write(line_string+'\n')
				else:
					with open(path_new_annot+'/'+file_dir+'_frame'+str(frame)+'.txt','w') as new_annot_file_txt:
						new_annot_file_txt.write(line_string+'\n')

