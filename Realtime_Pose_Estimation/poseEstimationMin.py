import cv2
import mediapipe as mp
import math
from playsound import playsound
import threading

Repeat = 0
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def song():
    global Repeat
    Repeat = 1
    playsound('erika.mp3')
    Repeat = 0

def calculateDistance(landmark1, landmark2):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    distance = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
    return distance

def calculateAngle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1-x2))
    if angle < 0:
        angle += 360
    return angle


def classifyPose(landmarks, output_image):
    label = "unknown pose"
    color = (0, 0, 255)

    left_elbow_angle = calculateAngle(landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mpPose.PoseLandmark.LEFT_WRIST.value])


    right_elbow_angle = calculateAngle(landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value])

    left_shoulder_angle = calculateAngle(landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mpPose.PoseLandmark.LEFT_HIP.value])


    right_shoulder_angle = calculateAngle(landmarks[mpPose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value])


    left_knee_angle = calculateAngle(landmarks[mpPose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mpPose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mpPose.PoseLandmark.LEFT_ANKLE.value])

    right_knee_angle = calculateAngle(landmarks[mpPose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value])

    handNoseDistance = calculateDistance(landmarks[mpPose.PoseLandmark.NOSE.value],
                                         landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value])

    sholderWristDistance = calculateDistance(landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value],
                                         landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value])

    x, y, _ = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value]
    output_image = cv2.circle(output_image, (x, y), 1, (0, 255, 0), 5)
    
    if ( left_shoulder_angle < 20 and left_shoulder_angle > 10) and (right_shoulder_angle < 100 and right_shoulder_angle > 90 ) and (left_elbow_angle > 250 and left_elbow_angle < 280 ) and (right_elbow_angle > 170 and right_elbow_angle < 195 ):
        label = "Hitler"

    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:
        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:
            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
                if left_knee_angle > 90 and left_knee_angle > 120 or right_knee_angle > 90 and right_knee_angle < 120:
                    label = 'Warrior II Pose'
            if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:
                label = 'T Pose'
    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:
            label = 'Tree Pose'

    if (handNoseDistance < 187 and handNoseDistance > 130) and handNoseDistance > 20:
        if ( sholderWristDistance < 140 and sholderWristDistance > 120):
            label = "hitler"

    if label != 'Unknown Pose':
        color = (0, 0, 255)
    cv2.putText(output_image, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    return output_image, label


cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    landmarks = []
    height, width, _ = img.shape
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:

            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                              (landmark.z * width)))
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img, current_pose = classifyPose(landmarks, img)
        if current_pose == "Hitler":
            if Repeat == 0:
                thread = threading.Thread(target=song, args=(), daemon=True)
                thread.start()

    cv2.imshow('output', img)
    k = cv2.waitKey(1) & 0xff
    if k == 27 :
        break

cv2.destroyAllWindows()
