import cv2

cap = cv2.VideoCapture(0)

height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

def draw_recangle(event, x, y, flags, param):
    global pt1, pt2, top_left, bottom_right

    if event == cv2.EVENT_LBUTTONDOWN:

        if top_left == True and bottom_right == True:
            pt1 = (0,0)
            pt2 = (0,0)
            top_left = False
            bottom_right = False

        if top_left == False:
            pt1 = (x,y)
            top_left = True

        if bottom_right == False:
            pt2 = (x, y)
            bottom_right = True

pt1 = (0,0)
pt2 = (0,0)
top_left = False
bottom_right = False

cap = cv2.VideoCapture(0)
cv2.namedWindow('Test')
cv2.setMouseCallback('Test', draw_recangle)

while True:
    ret, frame = cap.read()

    if top_left:
        cv2.circle(frame, pt1, 5, (0,0,255), -1)

    if top_left and bottom_right:
        cv2.rectangle(frame, pt1, pt2, (0,0,255), 3)
    cv2.imshow('frame', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()