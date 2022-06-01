import cv2
import math
import numpy as np
import os
import pdb
import xml.etree.ElementTree as ET


class ImgAugemention():
    def __init__(self):
        self.angle = 90

    # rotate_img
    def rotate_image(self, src, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        # convet angle into rad
        rangle = np.deg2rad(angle)  # angle in radians
        # calculate new image width and height
        nw = round((abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale,2)
        nh = round((abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale,2)
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # map
        return cv2.warpAffine(
            src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))),
            flags=cv2.INTER_LANCZOS4)

    def rotate_xml(self, src, xmin, ymin, xmax, ymax, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        rangle = np.deg2rad(angle)  # angle in radians
        # now calculate new image width and height
        # get width and heigh of changed image
        nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
        nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # rot_mat: the final rot matrix
        # get the four center of edges in the initial martix，and convert the coord
        point1 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymin, 1]))
        point2 = np.dot(rot_mat, np.array([xmax, (ymin+ymax)/2, 1]))
        point3 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymax, 1]))
        point4 = np.dot(rot_mat, np.array([xmin, (ymin+ymax)/2, 1]))
        # concat np.array
        concat = np.vstack((point1, point2, point3, point4))
        # change type
        concat = concat.astype(np.int32)
        # print(concat)
        rx, ry, rw, rh = cv2.boundingRect(concat)
        return rx, ry, rw, rh

    def process_img(self, imgs_path, xmls_path, img_save_path, xml_save_path, angle_list):
        # assign the rot angles

        for angle in angle_list:
            bbox=[]
            for img_name in os.listdir(imgs_path):
                # split filename and suffix
                n, s = os.path.splitext(img_name)
                # for the sake of use yolo model, only process '.jpg'
                if s == ".png":
                    img_path = os.path.join(imgs_path, img_name)
                    img = cv2.imread(img_path)
                    rotated_img = self.rotate_image(img, angle)
                    save_name = n + "_" + str(angle) + "d.png"
                    print(save_name,rotated_img.shape[0], rotated_img.shape[1], rotated_img.shape[2])
                    # 写入图像
                    cv2.imwrite(img_save_path + save_name, rotated_img)
                    # print("log: [%sd] %s is processed." % (angle, img))
                    xml_url = img_name.replace('Trainimage1/','Trainxml1/')
                    xml_url = xml_url .replace('.png', '.xml')
                    xml_path = os.path.join(xmls_path, xml_url)
                    tree = ET.parse(xml_path)
                    file_name = tree.find('filename').text  # it is origin name
                    #path = tree.find('path').text  # it is origin path
                    # change name and path
                    tree.find('filename').text = save_name  # change file name to rot degree name
                    #tree.find('path').text = save_name  #  change file path to rot degree name
                    root = tree.getroot()
                    if angle==90 or angle==270:
                        height=root.find('size').find('height').text
                        width = root.find('size').find('width').text
                        root.find('size').find('width').text=height
                        root.find('size').find('height').text=width
                    for box in root.iter('bndbox'):
                        xmin = float(box.find('xmin').text)
                        ymin = float(box.find('ymin').text)
                        xmax = float(box.find('xmax').text)
                        ymax = float(box.find('ymax').text)
                        x, y, w, h = self.rotate_xml(img, xmin, ymin, xmax, ymax, angle)
                        # change the coord
                        box.find('xmin').text = str(x)
                        box.find('ymin').text = str(y)
                        box.find('xmax').text = str(x+w)
                        box.find('ymax').text = str(y+h)
                        box.set('updated', 'yes')
                        bbox.append([x, y, x+w, y+h])


                    # write into new xml
                tree.write(xml_save_path + n + "_" + str(angle) + "d.xml")
                # for box in bbox:
                #     cv2.rectangle(rotated_img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                    # cv2.putText(rotated_img, str(box[4]), (box[0], max(20, box[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    #             (0, 0, 255), 2)

                # cv2.imshow(save_name , rotated_img)
                # cv2.waitKey(0)
                # bbox = []
                # print("[%s] %s is processed." % (angle, img_name))


if __name__ == '__main__':
    img_aug = ImgAugemention()
    path='VOCdevkit/VOC2007/'
    imgs_path=path+'Trainimage1/'
    xmls_path=path+'Trainxml1/'

    save_path='VOCdevkit/VOC2007/Rotate1/'
    img_save_path=save_path+'Trainimage1/'
    xml_save_path=save_path+'Trainxml1/'
    angle_list = [0,90,180,270]
    img_aug.process_img(imgs_path, xmls_path, img_save_path, xml_save_path, angle_list)
