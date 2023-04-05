import cv2
import time

cap = cv2.VideoCapture("sample1.mp4")

img = cv2.imread('fly64.png')

img_height, img_width, _ = img.shape

cap.set(3,1280)
cap.set(4,700)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations = 3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        x_coords = x + img_width
        y_coords = y+ img_height
        if x_coords >= 1280:
            x_coords -= 30
        if y_coords >= 720:
            y_coords -=30
        
        frame1[ y:y+img_height , x:x_coords] = img
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("frame1", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
    #time.sleep(0.1)




cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()