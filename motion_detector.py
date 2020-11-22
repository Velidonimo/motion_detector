import cv2
from datetime import datetime
import pandas


video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

comparing_frame = None
frame_counter = 0
detectings_list = [False, False]
times = []

while True:
    detecting_movement = False

    # getting the current_frame, uncoloring and blurring it
    check, current_frame = video.read()
    gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21,21), 0)

    # storing the first frame to compare the current frame with it
    # waiting a couple frames to warm the camera up
    if comparing_frame is None:
        frame_counter += 1
        if frame_counter > 50:
            comparing_frame = gray_frame
        continue

    delta_frame = cv2.absdiff(comparing_frame, gray_frame)
    thresh_delta_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # smoothing image a little by delating the white fields
    thresh_delta_frame = cv2.dilate(thresh_delta_frame, None, iterations=2)

    # finding contours of white areas bigger then 10000px(because I'm using a computer webcam. So everything is close)
    (cntrs, _) = cv2.findContours(thresh_delta_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in cntrs:
        if cv2.contourArea(contour) < 10000:
            continue
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(current_frame, (x,y), (x+w, y+h), (0,255,0), 3)
        detecting_movement = True
    detectings_list.append(detecting_movement)

    # saving time if we have changes in moving state
    if detectings_list[-1] != detectings_list[-2]:
        times.append(datetime.now())

    cv2.imshow('Current frame', current_frame)
    cv2.imshow("Delta frame", delta_frame)
    cv2.imshow("Thresh frame", thresh_delta_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        # adding quit-move state
        if detecting_movement:
            times.append(datetime.now())
        break

video.release()
cv2.destroyAllWindows()


# collect motions to dataframe
df = pandas.DataFrame(columns=["Start", "End"])
for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

