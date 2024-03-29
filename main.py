import cv2
import numpy as np
import argparse
import time

def create_files():
  num = 50 # cv2.aruco.DICT_4X4_50
  size = 1000 # pixel (w,h)

  for i in range(num):
    markerImage = np.zeros((size, size), dtype=np.uint8)
    markerImage = cv2.aruco.drawMarker(dictionary, i, size, markerImage, 1)
    cv2.imwrite("4x4_50/data{}.jpg".format(i), markerImage)
    time.sleep(0.05)
  print('Create files.')

def detect(img):
  marker_length = 0.02 # [m]
  camera_matrix = np.array( [[1.42068235e+03,0.00000000e+00,9.49208512e+02],
    [0.00000000e+00,1.37416685e+03,5.39622051e+02],
    [0.00000000e+00,0.00000000e+00,1.00000000e+00]] )
  distortion_coeff = np.array( [1.69926613e-01,-7.40003491e-01,-7.45655262e-03,-1.79442353e-03, 2.46650225e+00] )

  corners, ids, _ = cv2.aruco.detectMarkers(img, dictionary, parameters=parameters)
    
  res = []
  if len(corners) > 0:
    img = cv2.aruco.drawDetectedMarkers(img, corners, ids)
    ids = ids.flatten()

    for (corner, markerID) in zip(corners, ids): 
      rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, marker_length, camera_matrix, distortion_coeff)
      distance = int(tvec[0][0][2] * 100) #[cm]
      (topLeft, topRight, bottomRight, bottomLeft) = corner.reshape((4, 2))
      # convert each of the (x, y)-coordinate pairs to integers
      topRight = (int(topRight[0]), int(topRight[1]))
      bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
      bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
      topLeft = (int(topLeft[0]), int(topLeft[1]))
      #cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
      cv2.line(img, topLeft, topRight, (255, 0, 0), 4)
      cv2.line(img, topRight, bottomRight, (255, 0, 0), 4)
      cv2.line(img, bottomRight, bottomLeft, (255, 0, 0), 4)
      cv2.line(img, bottomLeft, topLeft, (255, 0, 0), 4)
      #cv2.putText(img, str(markerID),
      #            (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
      #            0.5, (0, 255, 0), 2)
      cX = int((topLeft[0] + bottomRight[0]) / 2.0)
      cY = int((topLeft[1] + bottomRight[1]) / 2.0)
      res.append({"id":markerID, "cX":cX, "cY":cY, "distance":distance})        

    #cv2.imshow("DEMO", img)
    #cv2.waitKey(1)

  return res


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', help='create|detect')
  args = parser.parse_args()

  dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
  parameters = cv2.aruco.DetectorParameters_create()

  if args.mode == 'create':
    create_files()
  if args.mode == 'detect':
    cap = cv2.VideoCapture(0)
    while True:
      s = time.time()
      _, img = cap.read()
      ret = detect(img)
      print(time.time()-s, ret)

