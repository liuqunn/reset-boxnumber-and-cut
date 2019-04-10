import cv2
import numpy as np
from math import *
import os
import json
import time
 

def  rotate_img(img,points):
    point1 = points[0]
    point2 = points[1]
    point3 = points[2]
    point4 = points[3]
    p1 = int(sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2))
    p2 = int(sqrt((point1[0]-point4[0])**2+(point1[1]-point4[1])**2))
    #判断长短边
    if p1 > p2:
        ##判断长边是水平还是竖直方向   
        angle = acos(abs(point1[0] - point2[0]) / p1) * (180 / pi)
        length = p1
        width = p2
        print(angle)
        #判断顺时针还是逆时针
        if (point1[1]-point2[1])/(point1[0]-point2[0])>0:
            print('333333333')
            if angle > 45:
                angle = -angle
        else:
            angle = -angle
    else:
        angle = acos(abs(point1[0] - point4[0]) / p2) * (180 / pi)
        length = p2
        width = p1
        print('11111111111')
        if (point1[1]-point4[1])/(point1[0]-point4[0])<0:
            angle += 90
        else:
            print('2222222222')
            angle -= 90
    print(angle)
    
    #中心点
    center_x = int((points[0][0]+points[1][0]+points[2][0]+points[3][0])/4)
    center_y = int((points[0][1]+points[1][1]+points[2][1]+points[3][1])/4)
    print(center_x,center_y)
    #裁剪图片
    x = []
    y = []
    for i in range(4):
        x.append(points[i][0])
        y.append(points[i][1])
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    img = img[y_min:y_max,x_min:x_max]
    print(img.shape[:2])
    #旋转
    rotateMat = cv2.getRotationMatrix2D((int(img.shape[:2][0]/2) , int(img.shape[:2][1]/2)), angle, 1)  
    imgRotation = cv2.warpAffine(img, rotateMat, (img.shape[:2][1], img.shape[:2][0]))
    cv2.imshow('img',img)
    cv2.imshow('imgRotation',imgRotation)
    #再次剪切去除多余部分
    #last_img = img[]
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ReadTxt(json_file):
    try:
        with open(json_file) as f:
            data = json.load(f)
            points = data['shapes'][3]['points']
            points = np.array(points)
            print(points)
        return points
    except:
        print('没有此%s文件'%json_file)
        
 
if __name__=="__main__":
    start = time.clock() 
    dir = "C:/Users/zh/Desktop/LandLeft/"
    listdir = os.listdir(dir)
    for i in listdir:
        img_path = dir + i 
        print(img_path)
        if img_path[-3:] == 'jpg':
            json_file = img_path.split('.')[0] + '.json'
            img = cv2.imread(img_path)    
            points = ReadTxt(json_file)
            rotate_img(img,points)
            elapsed = (time.clock() - start)
            print("Time used:",elapsed)