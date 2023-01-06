import numpy as np
import cv2
import glob

cameraMatrix = np.array([[2.21621389e+03 ,0 ,3.02566125e+02],[0 ,1.46865347e+03 ,2.62264299e+02],[0 ,0 ,1]])

# cameraMatrix = [[1137, 0,  320],[   0, 1413,  238],[   0,    0,    1]]

dist = np.array([[ 1.38033246e+00 ,-1.05277318e+02 ,-1.35525971e-02 ,-1.38221415e-01 ,9.85521515e+02]])

total_error = 0.8560972510208262

def calibration(img):
    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imshow('caliResult', dst)



vid = cv2.VideoCapture(0)
while (True):

    ret, frame = vid.read()
    cv2.imshow('orginal', frame)
    calibration(frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break