#Libraries
import cv2

cap =cv2.VideoCapture(0)

# Tracker
#tracker = cv2.legacy.TrackerMOSSE_create()
tracker = cv2.legacy.TrackerCSRT_create()

def drawLine(image, start_point, end_point, color, thickness):
    cv2.line(image, start_point, end_point, color, thickness)

def findCenter(bbox):
    X_Coordinate, Y_Coordinate, Width, Height = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    centerX , centerY = X_Coordinate + (Height / 2) , Y_Coordinate + (Width / 2)
    return centerX, centerY

def drawBox(image,bbox):
    X_Coordinate, Y_Coordinate, Width, Height = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(image,(X_Coordinate,Y_Coordinate),((X_Coordinate + Width),(Y_Coordinate + Height)),(255,0,255),3,1)

def position(X_val, Y_val):
    if (X_val > 0 and Y_val > 0) and (X_val <= 213 and Y_val <= 160):
        print("Top Left")
    if (X_val > 213 and Y_val > 0) and (X_val <= 426 and Y_val <= 160):
        print("Top Middle")
    if (X_val > 426 and Y_val > 0) and (X_val <= 640 and Y_val <= 160):
        print("Top Right")

    if (X_val > 0 and Y_val > 160) and (X_val <= 213 and Y_val <= 320):
        print("Middle Left")
    if (X_val > 213 and Y_val > 160) and (X_val <= 426 and Y_val <= 320):
        print("Center")
    if (X_val > 426 and Y_val > 160) and (X_val <= 640 and Y_val <= 320):
        print("Middle Right")
    if (X_val > 0 and Y_val > 320) and (X_val <= 213 and Y_val <= 640):
        print("Bottom Left")
    if (X_val > 213 and Y_val > 320) and (X_val <= 426 and Y_val <= 640):
        print("Bottom Middle")
    if (X_val > 426 and Y_val > 320) and (X_val <= 640 and Y_val <= 640):
        print("Bottom Right")


while True:
    success, img = cap.read()
    bbox = cv2.selectROI("Tracking",img,False)
    if bbox != (0, 0, 0, 0):
        tracker.init(img,bbox)
        break
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


while True:
    timer = cv2.getTickCount()
    success,img =cap.read()

    trackerSuccess,bbox = tracker.update(img)

    drawLine(img, (0, 160), (640, 160), (0, 0, 255), 1)
    drawLine(img, (0, 320), (640, 320), (0, 0, 255), 1)
    drawLine(img, (213, 0), (213, 480), (0, 0, 255), 1)
    drawLine(img, (426, 0), (426, 480), (0, 0, 255), 1)

    if trackerSuccess:
        drawBox(img,bbox)
        X_val, Y_val = findCenter(bbox)
        position(X_val, Y_val)

    else:
        cv2.putText(img,"Object Lost",(6,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow("Tracking", img)
        if cv2.waitKey(0) & 0xff == ord('q'):
            break

    fps = int(cv2.getTickFrequency()/(cv2.getTickCount()-timer))
    cv2.putText(img,str(fps),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow("Tracking",img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break