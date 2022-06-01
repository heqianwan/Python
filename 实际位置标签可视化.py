import cv2
import os
from tqdm import tqdm

def val_visual_results():
    txt_path="data/VOCdevkit/VOC2007/ImageSets/Main/val.txt"
    images_path="data/VOCdevkit/VOC2007/JPEGImages/"
    val_visual_path='data/valvisual_txt/'
    val_detect_path='UpdateResults/updateresult/'
    save_image=''
    txt_file=open(txt_path)
    for line in txt_file.readlines():
        line=line.strip('\n')
        if not (os.path.exists(images_path+line+'.jpg') or os.path.exists(images_path+line+'.jpeg') or os.path.exists(images_path+line+'.png')):
            continue
        if os.path.exists(images_path+line+'.jpg'):
            image=cv2.imread(images_path+line+'.jpg')
            save_image=line+'.jpg'
        elif os.path.exists(images_path+line+'.jpeg'):
            image=cv2.imread(images_path+line+'.jpeg')
            save_image=line+'.jpeg'
        else:
            image = cv2.imread(images_path + line + '.png')
            save_image = line + '.png'
        for line1 in open(val_visual_path+line+'.txt'):
            bb=line1.split(' ')
            label = bb[0]
            score = bb[1]
            xmin = bb[2]
            ymin = bb[3]
            xmax = bb[4]
            ymax = bb[5]
            cv2.rectangle(image, (int(float(xmin)), int(float(ymin))), (int(float(xmax)), int(float(ymax))),
                          (0, 0, 255), 1)
            cv2.putText(image, label, (int(float(xmin)) + 10, int(float(ymin)) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1)
        if os.path.exists(val_detect_path+line+'.txt'):
            for line2 in open(val_detect_path+line+'.txt'):
                bb = line2.split(' ')
                label = bb[0]
                score = bb[1]
                xmin = bb[2]
                ymin = bb[3]
                xmax = bb[4]
                ymax = bb[5]
                cv2.rectangle(image, (int(float(xmin)), int(float(ymin))), (int(float(xmax)), int(float(ymax))),
                              (0, 255, 0), 1)
                cv2.putText(image, label, (int(float(xmin)) + 10, int(float(ymin)) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 1)

        cv2.imwrite("Visual_val/" +save_image, image)

if __name__ == '__main__':
   val_visual_results()









