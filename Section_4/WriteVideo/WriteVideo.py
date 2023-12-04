import cv2

cap = cv2.VideoCapture(4) #default camera

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

writer = cv2.VideoWriter("Videos", cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height)) #divx for windows

while True:
    ret, frame = cap.read()

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    writer.release()
    cap.release()
    cv2.destroyAllWindows()