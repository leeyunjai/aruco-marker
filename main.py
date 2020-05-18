import cv2
import numpy as np
import argparse
import time

def create_files():
  num = 50 # cv2.aruco.DICT_4X4_50
  size = 200 # pixel (w,h)

  for i in range(num):
    markerImage = np.zeros((size, size), dtype=np.uint8)
    markerImage = cv2.aruco.drawMarker(dictionary, i, size, markerImage, 1)
    cv2.imwrite("data/data{}.jpg".format(i), markerImage)
    time.sleep(0.05)
  print('Create files.')

def detect():
  cap = cv2.VideoCapture(0)
  
  while(True):
    _, img = cap.read()
    _c, _ids, _ = cv2.aruco.detectMarkers(img, dictionary, parameters=parameters)
    img = cv2.aruco.drawDetectedMarkers(img, _c, _ids)
    cv2.imshow("DEMO", img)
    cv2.waitKey(1)
   
if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', help='create|detect')
  args = parser.parse_args()

  dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
  parameters = cv2.aruco.DetectorParameters_create()
  
  if args.mode == 'create':
    create_files()
  if args.mode == 'detect':
    detect()
