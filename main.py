#This is for clint
import socket
import cv2
import numpy as np
import smtplib
#import matplotlib.pyplot as plt

import time
de=0
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#q = input("Enter the ip address from where you want to receive the image")
#p = int(input("Enter the port number"))
s = "images.jpg"
print(s)
condition = True
c.connect(("192.168.1.97",4567))
f = open(s,"wb")
while condition:
    image = c.recv(1024)
    if str(image) == "b''":
        condition = False
    f.write(image)
    de=1


if(de == 1):

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()

    lower_bound = np.array([0, 0, 150])
    upper_bound = np.array([80, 80, 255])

    frame = cv2.imread("images.jpg")

    frame = cv2.resize(frame, (1280, 720))
    frame = cv2.flip(frame, 1)

    frame_smooth = cv2.GaussianBlur(frame, (7, 7), 0)

    mask = np.zeros_like(frame)

    mask[0:720, 0:1280] = [255, 255, 255]

    img_roi = cv2.bitwise_and(frame_smooth, mask)

    frame_hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)

    image_binary = cv2.inRange(frame_hsv, lower_bound, upper_bound)

    check_if_fire_detected = cv2.countNonZero(image_binary)

    if int(check_if_fire_detected) >= 2000:
        cv2.putText(frame, "Fire Detected !", (300, 60), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
        cv2.imwrite("onur.jpg",frame)
        content = "fire detected"
   # cv2.imshow("Fire Detection", frame)

    else:
        content = "fire not detected"




    mail.login("estu.okta1@gmail.com", "estu.okta.26")
    mail.sendmail("estu.okta1@gmail.com", "onurcanzengin@hotmail.com", content)