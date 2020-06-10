import cv2
import imutils

capture = cv2.VideoCapture('videos/Megamind.avi');
i = 0

while True:
    ret, frame = capture.read()

    if ret:
        # print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        # print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        (h, w, d) = frame.shape
        print("width={}, height={}, depth={}".format(w, h, d))

        if i < 100:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # resized = imutils.resize(image, width=300)     # auto calculate aspect ratio
        # rotated = imutils.rotate(image, -45)   # rotate
        if i < 150:
            frame = imutils.rotate_bound(frame, 45)  # rotate bound(entire image in view)

        # (h, w) = frame.shape[:2]
        # center = (h / 2, w / 2)
        # M = cv2.getRotationMatrix2D(center, 180, 1)
        # rotated = cv2.warpAffine(frame, M, (w, h))

        # blurred = cv2.GaussianBlur(image, (11, 11), 0)    # blur,  11 x 11 kernel,
        # Larger kernels would yield a more blurry image
        # output = image.copy()  # copy of original image

        if i < 250:
            frame = frame[100:400, 0:400]

        cv2.imshow('frame', frame)

        cv2.imwrite('Video_frames' + str(i) + '.jpg', frame)
        i += 1

        if cv2.waitKey(1) == ord('q'):
            break

    else:
        break

capture.release()
cv2.destroyAllWindows()
