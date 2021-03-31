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
    corners, ids, _ = cv2.aruco.detectMarkers(img, dictionary, parameters=parameters)

    if len(corners) > 0:
      # flatten the ArUco IDs list
      ids = ids.flatten()
      # loop over the detected ArUCo corners
      for (markerCorner, markerID) in zip(corners, ids):
        # extract the marker corners (which are always returned in
        # top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        cv2.rectangle(img, topLeft, bottomRight, (255,0,0), 2)

        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the image
        cv2.putText(img, str(markerID),
                    (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)

    #img = cv2.aruco.drawDetectedMarkers(img, _c, _ids)
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
