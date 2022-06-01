import xml.etree.ElementTree as ET
import os
import cv2
def xml_visuals():
    xml_files='data/b52xml/'
    srcimage_files='data/b52/'
    dstimage_files='shiyan/'
    if not os.path.exists(dstimage_files):
        os.mkdir(dstimage_files)
    for imagefile in os.listdir(srcimage_files):
        print(imagefile)
        imagename=imagefile.split('.')[0]
        xmlfile=imagename+'.xml'
        if not os.path.exists(xml_files+xmlfile):
            continue
        image=cv2.imread(srcimage_files+imagefile)
        tree=ET.parse(xml_files+xmlfile)
        root=tree.getroot()
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if  int(difficult) == 1:
                continue
            xmlbox = obj.find('bndbox')
            xmin=int(float(xmlbox.find('xmin').text))
            ymin = int(float(xmlbox.find('ymin').text))
            xmax = int(float(xmlbox.find('xmax').text))
            ymax = int(float(xmlbox.find('ymax').text))
            cv2.rectangle(image, (xmin,ymin),(xmax,ymax), (255, 255, 0), 1)
            cv2.putText(image, cls, (xmin+ 10, ymin + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 0), 1)
        cv2.imwrite(dstimage_files + imagefile, image)
if __name__=='__main__':
    xml_visuals()
