# To obtain the values/detais of the camera\video

import cv2
vcap = cv2.VideoCapture(0)
#path = 'location/file.mp4'
# vcap = cv2.VideoCapture(path)


if vcap.isOpened():
    width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)  # Width
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Height
    fps = vcap.get(cv2.CAP_PROP_FPS) # Fps
    frame_count = vcap.get(cv2.CAP_PROP_FRAME_COUNT)

    print('Width, Height: ', width, height)
    print('fps:', fps)
    print('frames count:', frame_count)  # Frame_count
