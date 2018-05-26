#Imports
import argparse
import cv2
import os

#Main method
if __name__ == "__main__":

    #Variables
    counter = 0
    counter_images = 0
    frame_rate = 15
    
    parser = argparse.ArgumentParser(description='Process a video.')
    parser.add_argument('path', metavar='video_path', type=str,
                        help='Path to source video')

    args = parser.parse_args()
    print("Source Path:", args.path)
    cap = cv2.VideoCapture(args.path)

    directory = 'images_from_video_'+args.path

    if not os.path.exists(directory):
    	os.makedirs(directory)
    
    video_name = args.path.split('.')[0]
    while True:
        
        r, frame = cap.read()
       
        if r:

            counter += 1

            if(counter%frame_rate == 0):
                counter_images += 1
                cv2.imwrite(directory+'/'+video_name+'-'+str(counter).rjust(5,'0')+'.jpg',frame)
                print('imagen '+str(counter_images)+' creada')
        else:
            break
