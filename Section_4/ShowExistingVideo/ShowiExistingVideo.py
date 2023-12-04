import cv2
import time

cap = cv2.VideoCapture("Video Direction")

if cap.isOpened() == False:
    print("Folder not found or wrong codec used!")

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:

        time.sleep(1/20) #1/FPS
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
