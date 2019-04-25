import cv2
import json
import os
import numpy as np
from math import *
import time

def mask_pic(img,lists,data):
    for i in range(len(lists)):
        points = lists[i]
        #print('points',points)
        label = data['shapes'][i]['label']
        #print('label',label)
        print('pic_path',img_path)
        #标签在列表中不进行操作，进行下一次循环
        labels = ["SEAL", "D","D1", "D2","D3","D4","D5","D6","D7","D8","D9"]
        if label in labels:
            continue
        #如果形状为rectangle（铅封）不进行操作，跳过
        if data['shapes'][i]['shape_type'] == 'rectangle':
            continue
        b  = np.array([[[points[0]],  [points[1]], [points[2]],[points[3]]]], dtype = np.int32)
        im = np.zeros(img.shape[:2], dtype = "uint8")
        cv2.polylines(im, b, 1, 255)
        #cv2.imshow('im',im)
        cv2.fillPoly(im, b, 255)
        #cv2.imshow('img',im)
        masked = cv2.bitwise_and(img, img, mask=im)
        # cv2.namedWindow("enhanced",0);
        # cv2.resizeWindow("enhanced", 640, 480);
        # cv2.imshow("enhanced", masked)
        # # #cv2.imshow("enhanced", img)
        # cv2.waitKey(0)
        #判断旋转角度
        point1 = points[0]
        point2 = points[1]
        point3 = points[2]
        point4 = points[3]
        p1 = sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)         
        p2 = sqrt((point1[0]-point4[0])**2+(point1[1]-point4[1])**2) 
        #判断长短边
        if p1 > p2:
            ##判断长边是水平还是竖直方向   
            angle = acos(abs(point1[0] - point2[0]) / p1) * (180 / pi)    
            length = int(p2)
            width = int(p1)
            print(angle)
            #判断顺时针还是逆时针
            if (point1[1]-point2[1])/(point1[0]-point2[0])>0:
                length = int(p2)
                width = int(p1)
                if angle > 45 :
                    print('333333333')
                    angle -= 90
                    length = int(p1)
                    width = int(p2)
            else:
                if  angle > 62:  #70 根据异常样本按需调整
                    print('44444444')
                    length = int(p1)
                    width = int(p2)
                    angle = 90 - angle 
                else:
                    print('555555555')
                    length = int(p2)
                    width = int(p1)
                    angle = -angle
        else:
            angle = acos(abs(point1[1] - point4[1]) / p2) * (180 / pi)
            if (point1[1]-point4[1])/(point1[0]-point4[0])<0:
                print('11111111111') 
                length = int(p1)
                width = int(p2)
                if angle > 70:   #70根据异常样本按需调整
                    angle = angle - 90
                else:
                    print("88888")
                    length = int(p2)
                    width = int(p1)
            else:
                length = int(p2)
                width = int(p1)
                print('2222222222')
                angle = -angle
        #print(angle)
    
        #中心点
        center_x = int((point1[0]+point2[0]+point3[0]+point4[0])/4)
        center_y = int((point1[1]+point2[1]+point3[1]+point4[1])/4)
        #旋转
        rotateMat = cv2.getRotationMatrix2D((center_x , center_y), angle, 1) 
        imgRotation = cv2.warpAffine(masked, rotateMat, (masked.shape[:2][1],masked.shape[:2][0]))
        #cv2.imwrite('C:/Users/zh/Desktop/rty/11'+label+'_'+picname,imgRotation)
        # cv2.imshow('imgrotate',imgRotation)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        left_x = abs(int(center_x - width/2))
        left_y = abs(int(center_y - length/2))
        right_x = abs(int(center_x + width/2))
        right_y = abs(int(center_y + length/2))

        last_img = imgRotation[left_y:right_y,left_x:right_x]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite('C:/Users/zh/Desktop/13/'+label+'_'+picname,last_img)

#读取json文件
def ReadTxt(json_file):
     try:
        with open(json_file) as f:
            data = json.load(f)
            lists = []
            for i in range(len(data['shapes'])):
                points = data['shapes'][i]['points']
                points = np.array(points)              
                lists.append(points)
            #print(lists)                
            return lists,data
     except:
        print('没有此%s文件'%json_file)

if __name__=="__main__":
    #要读取的文件夹路径
    dir = "C:/Users/zh/Desktop/err/"
    listdir = os.listdir(dir)
    for i in listdir:
        img_path = dir + i 
        picname = i
        print('img_path',img_path)
        #获得json文件路径
        if img_path[-3:] == 'jpg':
            json_file = img_path[0:-4] + '.json'
            #print('josn_file',json_file)
            lists,data = ReadTxt(json_file)
            start = time.clock()
            img = cv2.imread(img_path)    
            mask_pic(img,lists,data)
            elapsed = (time.clock() - start)
            print("Time used:",elapsed)
    