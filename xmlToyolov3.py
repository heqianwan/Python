import os
import xml.etree.ElementTree as ET
def convert(size, box):
    """
    convert(xmin, ymin, xmax, ymax) to (x, y, w, h)
    normalize x,y,w,h with width and height of the picture

    :param size: (w, h) of image
    :param box: (xmin, xmax, ymin, ymax)
    :return:
    """
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def xmltoyolo():
    xmlfiles='VOCdevkit/VOC2007/Trainxml/'
    yolofiles='shiyan/'
    classes=['c17','f22']
    if not os.path.exists(yolofiles):
        os.mkdir(yolofiles)
    for xmlfile in os.listdir(xmlfiles):
        xmlname=xmlfile.split('.')[0]
        yolofile=open(yolofiles+xmlname+'.txt','w')
        tree=ET.parse(xmlfiles+xmlfile)
        root=tree.getroot()
        size=root.find('size')
        h=int(size.find('height').text)
        w=int(size.find('width').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            yolofile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__=='__main__':
    xmltoyolo()