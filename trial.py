import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import math


def distance(point_1,point_2):
    x1,x2 = point_1[0],point_2[0]
    y1,y2 = point_1[1],point_2[1]

    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)

def corrdinates (cordinates_sorted,image,location,todo):

    arr1 = cordinates_sorted[0]
    point_0_0 = arr1[location[0]]
    point_1_0 = arr1[location[1]]
    point_2_0 = arr1[location[2]]
    point_3_0 = arr1[location[3]]
    arr1 = cordinates_sorted[1]
    point_0_1 = arr1[location[0]]
    point_1_1 = arr1[location[1]]
    point_2_1 = arr1[location[2]]
    point_3_1 = arr1[location[3]]
    arr1 = cordinates_sorted[2]
    point_0_2 = arr1[location[0]]
    point_1_2 = arr1[location[1]]
    point_2_2 = arr1[location[2]]
    point_3_2 = arr1[location[3]]
    arr1 = cordinates_sorted[3]
    point_0_3 = arr1[location[0]]
    point_1_3 = arr1[location[1]]
    point_2_3 = arr1[location[2]]
    point_3_3 = arr1[location[3]]

    if todo == 1:
        print(int(distance(point_0_0,point_1_0)))
        image = cv2.line(image, point_0_3, point_3_0, (0,0,255), 5)
        image = cv2.line(image, point_2_1, point_3_0, (255, 0, 0), 5)
        image = cv2.line(image, point_2_1, point_1_2, (0, 255, 0), 5)
        image = cv2.line(image, point_1_2, point_0_3, (0,255, 255), 5)
        return image
    if todo == 2:

        return warpPerspectivecrop(point_1_0,point_0_1,point_3_2,point_2_3)



def warpPerspectivecrop(pt_A ,pt_B ,pt_C ,pt_D ):
    width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    maxWidth = max(int(width_AD), int(width_BC))
    height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    maxHeight = max(int(height_AB), int(height_CD))
    input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
    output_pts = np.float32([[0, 0],
                             [0, maxHeight - 1],
                             [maxWidth - 1, maxHeight - 1],
                             [maxWidth - 1, 0]])
    M = cv2.getPerspectiveTransform(input_pts, output_pts)
    output_img = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
    return output_img


vid = cv2.VideoCapture(0)
parameters = aruco.DetectorParameters_create()
path = r'D:\Downloads\print_page-0001.jpg'

# Using cv2.imread() method
img = cv2.imread(path)
# while (True):

    # ret, frame = vid.read()
    # # cv2.imshow('frame', frame)
    #
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
frame = img
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

int_corners = np.int0(corners)
# cv2.polylines(frame,int_corners,True,(0,0,255),5)
cv2.imshow("hi", frame_markers)
arr = [1,0,3,2]
pos = []
i = 0
j = 0
print(ids)
for i in range (len(ids)):
    for j in range(len(arr)):
        if ids[i] == arr[j]:
            pos.append(j)
            print("id:"+str(arr[j]) + " at " + str(i)+"th position")
            j+= 1
        j =0
print(pos)

print(corners)
#
# print(corners[0])
#
# arrays = corners[0]

print("test")
# print(arrays[0][1])

# while True:
#     for id in range (len(ids)):
#         print(i)
#         for j in range (1):
#             arrays = int_corners[id]
#             print(arrays[0][j])
#             point = arrays[0][j]
#             cv2.circle(frame_markers,(point[0],point[1]) , 1, (0, 0, 255),6)
#             cv2.imshow("hi", frame_markers)
#


cordinates_sorted = []
for j in range(4):
    arr_eachpoint = []
    for id in range(len(ids)):
        arrays = int_corners[id]
        print(arrays[0][j])
        point = arrays[0][j]
        arr_eachpoint.append(arrays[0][j])
    cordinates_sorted.append(arr_eachpoint)
showline = corrdinates(cordinates_sorted,frame_markers,pos,1)
crop = corrdinates(cordinates_sorted,frame_markers,pos,2)
#
    # cv2.circle(showline, (point[0], point[1]), 1, (0, 0, 255), 6)
while True:
    cv2.imshow("hi", showline)
    cv2.imshow("by", crop)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break














# if ids is not None:
#     print("ids")
#     print(ids)
#
#     if ids[0]:
#         print("ids[0]")
#         print(ids[0])
#     if ids[1] is not None:
#         print("ids[1]")
#         print(ids[1])


    # if ids is not None:
    #     array1 = int_corners
    #     print("array1")
    #     print(array1)
    #     array2 = array1[0]
    #     print("array2")
    #     print(array2)
    #     array3 = array2[0]
    #     print("array3")
    #     print(array3)
    #     array4 = array3[0]
    #     print("array4")
    #     print(array4)
    #     array5 = array4[0]
    #     print("array5")
    #     print(array5)


vid.release()
# Destroy all the windows
cv2.destroyAllWindows()