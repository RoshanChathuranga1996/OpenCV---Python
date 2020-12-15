import cv2
import imagehash
import os
from PIL import Image
from datetime import datetime
from func import dHash, convert_hash


streamFrameNo = 0
# Stream
path = "E:\\Opencv_project\\Videos\\Stream\\d2.mp4"
capture = cv2.VideoCapture(0)

while True:
    global streamFld, endSF, startSF, t, configLoc
    ret, frame = capture.read()

    if ret:

        frame = frame[100:400, 0:640]
        checkD = dHash(frame)
        checkD = convert_hash(checkD)

        img2 = Image.fromarray(frame)
        check = imagehash.phash(img2)
        print("-- Processing frame {} --".format(streamFrameNo))

        now = datetime.now()
        nowStr = datetime.date(datetime.now()).strftime("%Y%b%d")
        nowLoc = str(now.date()) + " " + str(now.hour)
        ff = "{}".format(nowLoc)
        SFld = r'E:\\Opencv_project\\StreamTxt\\{}'.format(nowStr)  # path
        if not os.path.exists(SFld):
            os.makedirs(SFld)

        file_h = open(SFld + "\\{}.txt".format(ff), 'a+')
        file_h.write(str(datetime.now().time()) + " " + str(streamFrameNo) + " " + "{} {}\n".format(check, checkD))
        file_h.close()

        stream = r'E:\\Opencv_project\\Frames\\Set01\\Stream'  # path
        if not os.path.exists(stream):
            os.makedirs(stream)

        # txtAd = "Hash = {}".format(check)
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # frame = cv2.putText(frame, txtAd, (40, 40), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        # cv2.imwrite(stream + "\\" + str(streamFrameNo) + '.jpg', frame)

        streamFrameNo += 1

    else:
        break

capture.release()
cv2.destroyAllWindows()