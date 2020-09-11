import cv2
import imagehash
import pickle
from datetime import datetime
import numpy as np
from PIL import Image
from AdHash import logger1, logger2, logger3, nested_key, adName
import time
import os


hashes = pickle.loads(open('E:\\Opencv_project\\Pkl\\hashes.pickle', 'rb').read())
mainStart = time.time()
adName = list(adName.values())

subAdHash = {}
checkDict = {}
streamImg = {}
checkDictList = []
subAdHashList = []
status = 0
adFrameNo = 1
streamFrameNo = 0
matchCount = 1
missMatchCount = 0
missMatchCounterFinal = 0
totalFrameCounter = 0


def hamming(a, b):
    string1 = str(a)
    string2 = str(b)
    distance = 0
    lnt = len(string1)

    for y in range(lnt):
        if string1[y] != string2[y]:
            distance += 1

    return distance


# File location of stream
path = "E:\\Opencv_project\\Videos\\Stream\\Stream[test02].mp4"
capture = cv2.VideoCapture(path)

if not os.path.exists(path):
    logger2.error("Can't find stream !")

# get stream name
head_tail = os.path.split(path)
name = head_tail[1]

while True:
    global streamFld, endSF, startSF, t, pre
    ret, frame = capture.read()

    if ret:

        # frame = frame[200:850, 240:1680]
        frame = frame[200:850, 0:1920]
        # convert nd array to img
        img2 = Image.fromarray(frame)
        check = imagehash.phash(img2)
        print("-- Processing frame {} --".format(streamFrameNo + 1))

        # encoding
        img_encode = cv2.imencode('.jpg', frame)[1]
        data_encode = np.array(img_encode)
        byt_encode = data_encode.tobytes()

        m = {(streamFrameNo+1): byt_encode}
        # streamImg.update(m)

        # create folder for stream
        stream = r'E:\\Opencv_project\\Frames\\Set01\\{}'.format(name)
        if not os.path.exists(stream):
            os.makedirs(stream)

        # write stream frames
        txtAd = "Hash = {}".format(check)
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(frame, txtAd, (40, 40), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite(stream + "\\Frame " + str(streamFrameNo+1) + '.jpg', frame)

        streamFrameNo += 1

        if status == 0:

            adCounter = 0
            # check each Ad for match frame
            for t in range(len(nested_key)):
                sb_dt = nested_key[t]

                # Get the frame hashes of matched Ad
                subAdHash.clear()
                subAdHash = hashes[sb_dt].copy()
                subAdHashList = subAdHash.values()
                subAdHashList = list(subAdHashList)

                adCounter += 1

                # check with first 30 frames of Ad
                for x in range(30):
                    subFrame = subAdHashList[x]
                    diff = hamming(check, subFrame)

                    if check == subFrame:
                        checkDict = subAdHash.copy()
                        checkDictList = checkDict.values()
                        checkDictList = list(checkDictList)

                        logger1.info("Match to Ad {}...".format(t + 1))
                        logger3.info("Match to Ad {}...".format(t + 1))

                        logger1.info("<< Working with Ad {} ({}) >>".format((t+1), adName[t]))
                        logger1.info('-------' * 5)
                        logger3.info("<< Working with Ad {} ({}) >>".format((t+1), adName[t]))
                        logger3.info('-------' * 5)

                        logger1.info("SF {} - match with AdF 1 - Dif = 0".format(streamFrameNo) + "   [Hash: " +
                                     str(check) + ']')
                        print("SF {} - match with AdF 1 - Dif = 0".format(streamFrameNo) + "   [Hash: " +
                              str(check) + ']')

                        imgSc = adCounter - 1
                        status = 1

                        currentDt = datetime.date(datetime.now()).strftime("%Y%b%d")
                        currentTm = datetime.time(datetime.now()).strftime("%I-%M-%S %p")
                        ff = "AD{} ({}) - {}, {}".format((t+1), adName[t], currentDt, currentTm)

                        # create folder for matched ad with current date & time
                        streamFld = r'E:\\Opencv_project\\Frames\\Set01\\Match_frames\\{}'.format(ff)
                        if not os.path.exists(streamFld):
                            os.makedirs(streamFld)

                        break

                # if adCounter == len(nested_key):
                    # print(" No match ")

        elif status == 1:

            if len(checkDictList) > adFrameNo:  # set limit

                # check with matched ad frames. starting from 2nd frame
                currentHash = checkDictList[adFrameNo]
                adFrameNo += 1

                # calculate hamming distance for similarity
                dif = hamming(currentHash, check)

                if adFrameNo == 2:
                    startSF = streamFrameNo-1

                if dif < 11:
                    matchCount += 1
                    logger1.info("SF {} - match with AdF ".format(streamFrameNo) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + "   [Hash: " + str(check) + ']')
                    print("SF {} - match with AdF ".format(streamFrameNo) + str(adFrameNo) + " - Dif = " +
                          str(dif) + "   [Hash: " + str(check) + ']')

                # check for matched Ad is really matched ?
                elif adFrameNo == 30:
                    if missMatchCount > 25:
                        print("-- This Ad not match to stream --")
                        status = 0

                elif dif >= 11:
                    logger1.info("SF {} - miss match with AdF ".format(streamFrameNo) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')
                    print("SF {} - miss match with AdF ".format(streamFrameNo) + str(adFrameNo) + " - Dif = " +
                          str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')

                    missMatchCount += 1

                # count frames for matched Ad
                if adFrameNo == len(checkDictList):
                    endSF = streamFrameNo
                    totalFrameCounter = len(checkDict.keys())
                    missMatchCounterFinal = missMatchCount
                    pre = ((totalFrameCounter - missMatchCount) / totalFrameCounter) * 100

                    logger1.info('-------' * 7)
                    logger1.info("Total frames of ad = {}".format(totalFrameCounter))
                    logger1.info("Matched frames = {}".format(totalFrameCounter-missMatchCount))
                    logger1.info("Miss matched frames = {}".format(missMatchCount))
                    logger1.info("Match percentage : {}%\n\n\n".format(round(pre, 2)))
                    logger3.info("Match percentage of Ad{} ({}): {}%\n\n\n".format((t + 1), adName[t], round(pre, 2)))

            else:
                # logger1.info("SF {} - no match".format(streamFrameNo))
                status = 0

    else:
        break

capture.release()

if totalFrameCounter > 0:
    # identify matched frames of stream
    # imgList = list(streamImg.values())
    # q = startSF - 31

    # write matched stream frames
   # for _ in range((endSF - startSF) + 61):
        # imgLct = imgList[q]
        # reImage = np.asarray(bytearray(imgLct), dtype="uint8")
        # reImage = cv2.imdecode(reImage, cv2.IMREAD_COLOR)
        # cv2.imwrite(streamFld + "\\Frame {}.jpg".format(q + 1), reImage)
        # q += 1

    print('-------' * 7)
    print("Total frames of ad = {}".format(totalFrameCounter))
    print("Matched frames = {}".format(totalFrameCounter - missMatchCount))
    print("Miss matched frames = {}".format(missMatchCount))
    print("Match percentage : {}%\n\n\n".format(round(pre, 2)))

elif totalFrameCounter == 0:
    logger1.info('-------' * 7)
    logger1.info("--Not found any match Ad--")


mainEnd = time.time()

print("Total time duration = {} seconds".format(round((mainEnd - mainStart), 2)))
logger1.info("Total time duration = {} seconds".format(round((mainEnd - mainStart), 2)))
