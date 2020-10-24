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
        if frame_counter > 20:
            comparing_frame = gray_frame
            continue
        else:
            frame_counter += 1
            continue

    delta_frame = cv2.absdiff(comparing_frame, gray_frame)
    thresh_delta_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # smoothing image a little by delating the white fields
    thresh_delta_frame = cv2.dilate(thresh_delta_frame, None, iterations=2)

    # cv2.imshow('Current frame', gray_frame)
    # cv2.imshow('Comparing', comparing_frame)
    cv2.imshow('Delta', thresh_delta_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
