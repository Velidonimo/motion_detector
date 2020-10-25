import cv2


video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

comparing_frame = None
frame_counter = 0

while True:
    # getting the current_frame, uncoloring and blurring it
    check, current_frame = video.read()
    gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21,21), 0)

    # storing the first frame to compare the current frame with it
    # waiting a couple frames to warm the camera up
    if comparing_frame is None:
        if frame_counter > 50:
            comparing_frame = gray_frame
            continue
        else:
            frame_counter += 1
            continue

    delta_frame = cv2.absdiff(comparing_frame, gray_frame)
    thresh_delta_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # smoothing image a little by delating the white fields
    thresh_delta_frame = cv2.dilate(thresh_delta_frame, None, iterations=2)

    # finding contours of white areas bigger then 1000px
    (cntrs, _) = cv2.findContours(thresh_delta_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in cntrs:
        if cv2.contourArea(contour) < 1000:
            continue
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(current_frame, (x,y), (x+w, y+h), (0,255,0), 3)


    cv2.imshow('Current frame', current_frame)
    # cv2.imshow('Comparing', comparing_frame)
    #cv2.imshow('Delta', thresh_delta_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
