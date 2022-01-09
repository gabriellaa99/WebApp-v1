# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 12:21:03 2021

@author: User
"""


import cv2
import numpy as np
import random as rng
import time
import os
from datetime import datetime
import pytz
from .models import Result
from.constant import UPLOAD_FOLDER, RETRIEVE_FOLDER, OUTPUT_FOLDER

rng.seed(12345)
pest=[]

def Detect(j,filename):
    global pest
    start = time.time()
#=================================== Load Images ======================================
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))  # Path file gambar (folder/nama file)
    img = cv2.resize(img, (0, 0), fx = 0.9, fy = 0.9)
    imCrop = img[208:778, 71:608]

#============================= HSV CLAHE Algorithm ============================================
    imCrop_hsv = cv2.cvtColor(imCrop, cv2.COLOR_BGR2HSV) 
    h, s, v = cv2.split(imCrop_hsv)

    clahe2 = cv2.createCLAHE(clipLimit = 1.4, tileGridSize=(5,5))
    clahe3 = cv2.createCLAHE(clipLimit = 1.4, tileGridSize=(5,5))

    s = clahe2.apply(s)
    v = clahe3.apply(v)

    im_hsv =  cv2.merge([h, s, v])
    im_hsv = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)
    im_gray = cv2.cvtColor(im_hsv, cv2.COLOR_BGR2GRAY)
    

    ret, th = cv2.threshold(im_gray,j,255,cv2.THRESH_BINARY_INV) #210-255

    _, contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
    
    
    drawing = np.zeros((th.shape[0], th.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv2.drawContours(drawing, contours_poly, i, color)
        cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
          (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)

    
    num = len(contours)
    pest.append(num-1)
    print('Pests Detected: ' + str(num-1))
    text = "Jumlah Whitefly: " + str(num-1)
    cv2.drawContours(imCrop, contours, -1, (0, 0, 255), 2)
    cv2.putText(imCrop, text, (20, 550),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.imshow('Blob Detection', imCrop)
    # cv2.imwrite(os.path.join(RETRIEVE_FOLDER, filename), img)  # Gambar di save di Path yang ditentukan

    end = time.time()
    print("Waktu Eksekusi: " + str(end-start) + " detik") #Print Waktu running
    cv2.waitKey(5)
    cv2.destroyAllWindows()

def Database (filename,t,w,d):
    result =    Result(
                image=os.path.join(OUTPUT_FOLDER, filename),
                total = t, #Total Pest
                whitefly = w, #Total Whitefly
                damage = d #Persentase kerusakan
                )
    return result

def process_image(filename):
    global pest
    print('========================================================')
    print('Detection Starting...')
    print('Detecting Whitefly...')
    Detect(200,filename) #THreshold 200 untuk whitefly
    print('========================================================')
    print('Detecting Other Pest...')
    Detect(60,filename) #Threshold 60 untuk haa lainnya
    print('========================================================')
    print('Calculating Damage...')
    w = pest[0]
    b = pest[1]
    t = w+b
    d = (w/t)
    print('========================================================')
    print('Damage done by pest: ' + str(d) + ' %')
    result = Database(filename,t,w,d) #Masukin data ke database
    print('Detection Finished')
    pest = []
    return result


