import cv2
import os
from tqdm import tqdm
def yolo_visual_results():
    image_path = 'plane/'
    image_files=os.listdir(image_path)

    results_path='label/'
    visual_path='Visual/'
    if not os.path.exists(visual_path):
        os.makedirs(visual_path)
    for image_file in image_files:
        image=cv2.imread(image_path+image_file)
        h,w,c=image.shape
        image_name=image_file.split('.')[0]
        if not os.path.exists(results_path+image_name+'.txt'):
            continue
        for line in open(results_path+image_name+'.txt'):
            aa=line.split(' ')
            label=aa[0]
            print(image_name)
            xmin= (float(aa[1])-float(aa[3])/2)*w
            ymin = (float(aa[2])-float(aa[4])/2)*h
            xmax = (float(aa[1])+float(aa[3])/2)*w
            ymax = (float(aa[2])+float(aa[4])/2)*h
            cv2.rectangle(image, (int(float(xmin)), int(float(ymin))), (int(float(xmax)), int(float(ymax))),(255, 255, 0), 1)
            cv2.putText(image, label, (int(float(xmin)) + 10, int(float(ymin)) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.imwrite(visual_path+image_file,image)

if __name__ == '__main__':
   yolo_visual_results()









