import numpy as np
import cv2, PIL
from cv2 import aruco
import pandas as pd
import math



def Perspective_wrap_crop(pt_A ,pt_B ,pt_C ,pt_D,img):
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



def corrdinates (cordinates_sorted,image,location):
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
    return warpPerspectivecrop(point_0_3, point_3_0, point_2_1, point_1_2, image)
    # return warpPerspectivecrop(     BL  ,    TL   ,   TR    ,   BR    , image)



Video = cv2.VideoCapture(0)
while (True):

    ret, frame = Video.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    cv2.imshow("Aruco_ID_marked", frame_markers)


    int_corners = np.int0(corners)
    arr = [1,0,3,2]  #order i need
    pos = []
    i = 0
    j = 0
    if ids is not None:
        for i in range (len(ids)):
            for j in range(len(arr)):
                if ids[i] == arr[j]:
                    pos.append(j)
                    print("id:"+str(arr[j]) + " at " + str(i)+"th position")
                    j+= 1
                j =0
        print(pos)
        if len(ids) == 4:
            cordinates_sorted = []
            for j in range(4):
                arr_eachpoint = []
                for id in range(len(ids)):
                    arrays = int_corners[id]
                    point = arrays[0][j]
                    arr_eachpoint.append(arrays[0][j])
                cordinates_sorted.append(arr_eachpoint)
            croped_image = corrdinates(cordinates_sorted,frame,pos,2)

            cv2.imshow("Croped_image", croped_image)


vid.release()
cv2.destroyAllWindows()
