import cv2
from matplotlib import pyplot as plt
import time

def image_processing():
    img = cv2.imread('variant-10.jpg')
    ret,thres1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
    images = [img,thres1]
    titles = ['original','threshold150']
    for i in range(2):
        plt.subplot(1,2,i+1),plt.imshow(images[i],vmin=0,vmax=255)
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()
    print('1')

def video_processing():
    cap = cv2.VideoCapture(1)
    down_points = (1280, 720)
    i = 0
    count = 0
    flag = True
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        #print(ret, thresh)

        contours, hierarchy = cv2.findContours(thresh,
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        st_x, st_y = 465,285
        cv2.rectangle(frame, (st_x+150, st_y+150),(st_x, st_y), (0, 255, 0), 2)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y),(x+w, y + h), (0, 255, 0), 2)
            if i % 2 == 0:
                a = x + (w // 2)
                b = y + (h // 2)
            if flag:
                if (a >=st_x and a<= (st_x + 150)):
                    if (b>=st_y and b<= (st_y + 150)):
                        flag = False
                        frame = cv2.flip(frame, 0)
                        count += 1
                #print(a, b)
            if (x >(st_x + 150)):
                flag = True
            if x <st_x:
                flag = True
                #count += 1

        cv2.imshow('frame', thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #print(count, flag)
        time.sleep(0.1)
        i += 1

    cap.release()

def video_dop_processing():
    
    cap = cv2.VideoCapture("sample.mp4")
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
        _, thresh = cv2.threshold(blur,30, 255, cv2.THRESH_BINARY)
        #dilated = cv2.dilate(thresh, None, iterations = 3)
        сontours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(сontours) > 0:
            c = max(сontours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            frame1[ y:y+img_height , x:x+img_width ] = img
            stroka = str(x) + ', ' + str(y)
                #cv2.putText(frame1, stroka, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

            
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("frame1", thresh)
        frame1 = frame2
        ret, frame2 = cap.read()
        time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#if __name__ == '__main__':
#image_processing()
video_dop_processing()
    #video_processing()
cv2.waitKey(0)
  
# closing all open windows
cv2.destroyAllWindows()
