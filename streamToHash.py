import cv2
import imagehash
import os
from PIL import Image
from datetime import datetime
from func import dHash, convert_hash


imagesArray = []
streamFrameNo = 0
# Stream
path = "E:\\Opencv_project\\Videos\\Stream\\d2.mp4"
capture = cv2.VideoCapture(0)


while True:
    global streamFld, endSF, startSF, t, configLoc, width, height
    ret, frame = capture.read()

    if ret:

        frame = frame[100:400, 0:640]
        checkD = dHash(frame)
        checkD = convert_hash(checkD)

        img2 = Image.fromarray(frame)
        check = imagehash.phash(img2)
        print("-- Processing frame {} --".format(streamFrameNo))

        now = datetime.now()
        nowTime = now.time()
        nowTime = str(nowTime.strftime("%H-%M-%S-%f"))
        nowStr = datetime.date(datetime.now()).strftime("%Y%b%d")
        nowLoc = str(now.date()) + " " + str(now.hour)
        ff = "{}".format(nowLoc)

        SFld = r'E:\\Opencv_project\\StreamHash\\{}'.format(nowStr)  # path
        if not os.path.exists(SFld):
            os.makedirs(SFld)

        file_h = open(SFld + "\\{}.txt".format(ff), 'a+')
        file_h.write(str(datetime.now().time()) + " " + str(streamFrameNo) + " " + "{} {}\n".format(check, checkD))
        file_h.close()

        stream = r'E:\\Opencv_project\\Frames\\Stream\\{}\\{}'.format(nowStr, ff)
        if not os.path.exists(stream):
            os.makedirs(stream)

        resized_image = cv2.resize(frame, (100, 50))
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(stream + "\\" + nowTime + '.jpg', gray_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        streamFrameNo += 1

    else:
        break

capture.release()
cv2.destroyAllWindows()
