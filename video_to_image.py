import cv2
import os

cam = cv2.VideoCapture("F:\\JI\\RESEARCH\\DATABASE\\wanggang\\ChineseFoodForGPT\\raw-videos\\xiaochaozhugan.mp4")

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

currentframe = 0

while(True):

    ret,frame = cam.read()

    if ret:
        if currentframe % 25 == 0:
            name = './data/frame' + str(currentframe//25) + '.jpg'
            print('Creating...' + name)
            frame = frame[0:300, 0:640]
            cv2.imwrite(name, frame)
    else:
        break
    currentframe += 1

cam.release()
cv2.destroyAllWindows()