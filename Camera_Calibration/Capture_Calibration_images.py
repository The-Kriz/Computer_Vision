import cv2

key = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)
count = 0
while True:
    try:
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            cv2.imwrite(filename=('Calibration_image'+str(count)+'.png'), img=frame)
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            count += 1

        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
