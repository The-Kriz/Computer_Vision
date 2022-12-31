import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import math


def distance(x1 , y1 , x2 , y2):
	return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)


vid = cv2.VideoCapture(0)
parameters = aruco.DetectorParameters_create()
while (True):

    ret, frame = vid.read()
    # cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    int_corners = np.int0(corners)
    # cv2.polylines(frame,int_corners,True,(0,0,255),5)
    cv2.imshow("hi",frame_markers)

    distance(x1, y1, x2, y2)




    # if ids is not None :
    #     plt.figure()
    #     plt.imshow(frame_markers)
    #     for i in range(len(ids)):
    #         c = corners[i][0]
    #         plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
    #     plt.legend()
    #     plt.show()
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()