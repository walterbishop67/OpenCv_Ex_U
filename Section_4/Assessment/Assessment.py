import cv2

def draw_circle(event, x, y, flags, param):
    global pt1, isClicked

    if event == cv2.EVENT_LBUTTONDOWN:
        pt1 = (x,y)
        isClicked = True

    if event == cv2.EVENT_LBUTTONUP:
        isClicked = False


pt1 = (0,0)
isClicked = False

cap = cv2.VideoCapture(0)
cv2.namedWindow('test')
cv2.setMouseCallback('test', draw_circle)

while True:

    ret, frame = cap.read()

    if isClicked:
        cv2.circle('frame', pt1, 50, (0,255, 0), thickness=5)

    cv2.imshow('test', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()