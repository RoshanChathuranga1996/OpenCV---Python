import cv2

capture = cv2.VideoCapture('videos/Megamind.avi');
i = 0

while(True):
    ret, frame = capture.read()

    if ret == True:
        print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', frame)

        cv2.imwrite('Video_frames'+str(i)+'.jpg', frame)
        i+= 1

        if cv2.waitKey(1) == ord('q'):
            break

    else:
        break

capture.release()
cv2.destroyAllWindows()


