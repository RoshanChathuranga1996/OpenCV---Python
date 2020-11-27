import cv2
import imagehash
import pickle
from datetime import datetime
import numpy as np
from PIL import Image
from AdSample import logger1, logger3, nested_key, adName
import time
import os


mainStart = time.time()
hashes = pickle.loads(open('E:\\Opencv_project\\Pkl\\hashes.pickle', 'rb').read())
adNum = list(adName.keys())
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
matchCounterFinal = 0
missMatchCounterFinal = 0
totalFrameCounter = 0
point = 0
# Define Ad key frames
kx1 = 867  # sn 1 - 60f
kx2 = 942  # sn 2 - 13f
kx3 = 972  # sn 3 - 72f
# kx4 = 802  # sn 4 - 21f
# kx5 = 823  # sn 5 - 13f
# Match count of each sn
sn1 = 0
sn2 = 0
sn3 = 0
sn4 = 0
sn5 = 0
# Define 1st matched stream frame
st = 0
# Define accepted different level
different = 3
# Active sn
active = 0


def hamming(a, b):
    string1 = str(a)
    string2 = str(b)
    distance = 0
    lnt = len(string1)

    for y in range(lnt):
        if string1[y] != string2[y]:
            distance += 1

    return distance


def matchAd(fNo, adNo, stNo, di, sn):
    global checkDict, checkDictList, status, streamFld, st
    st = fNo
    checkDict = subAdHash.copy()
    checkDictList = checkDict.values()
    checkDictList = list(checkDictList)

    logger1.info('-------' * 5)
    logger1.info("Match to Ad {}...".format(adNo))
    # logger3.info('-------' * 5)
    # logger3.info("Match to Ad {}...".format(adNo))

    logger1.info("<< Working with Ad {} ({}) >>".format(adNo, adName[adNo-1]))
    logger1.info('-------' * 5)
    logger3.info("<< Working with Ad {} ({}) sn {} with stream frame {} & Ad frame {} >>".format(adNo, adName[adNo-1],
                                                                                                 sn, stNo, fNo))
    logger3.info('-------' * 5)

    logger1.info("SF {} - match with AdF {} - Dif = {}".format(stNo, fNo, di))
    print("SF {} - match with AdF {} - Dif = {}".format(stNo, fNo, di))
    print("Matched with sn {}".format(sn))

    # imgSc = adCounter - 1
    currentDt = datetime.date(datetime.now()).strftime("%Y%b%d")
    currentTm = datetime.time(datetime.now()).strftime("%I-%M-%S %p")
    ff = "AD{} ({}) - {}, {}".format(adNo, adName[adNo-1], currentDt, currentTm)

    streamFld = r'E:\\Opencv_project\\Frames\\Set01\\Match_frames\\{}'.format(ff)
    if not os.path.exists(streamFld):
        os.makedirs(streamFld)


# Stream
path = "E:\\Opencv_project\\Videos\\Stream\\r1.mp4"
capture = cv2.VideoCapture(path)

while True:
    global streamFld, endSF, startSF, t, configLoc
    ret, frame = capture.read()

    if ret:

        frame = frame[100:400, 0:640]
        img2 = Image.fromarray(frame)
        check = imagehash.phash(img2)
        print("-- Processing frame {} --".format(streamFrameNo))

        file_h = open('E:\\Opencv_project\\Pkl\\Stream.pickle', 'w')
        file_h.write(str(pickle.dumps(check)))
        file_h.close()

        img_encode = cv2.imencode('.jpg', frame)[1]
        data_encode = np.array(img_encode)
        byt_encode = data_encode.tobytes()

        m = {streamFrameNo: byt_encode}
        streamImg.update(m)

        stream = r'E:\\Opencv_project\\Frames\\Set01\\Stream'
        if not os.path.exists(stream):
            os.makedirs(stream)

        txtAd = "Hash = {}".format(check)
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(frame, txtAd, (40, 40), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite(stream + "\\" + str(streamFrameNo) + '.jpg', frame)

        streamFrameNo += 1

        if status == 0:

            adCounter = 0
            for t in range(len(nested_key)):
                sb_dt = nested_key[t]
                x1 = kx1
                x2 = kx2
                x3 = kx3
                # x4 = kx4
                # x5 = kx5

                # Get the frames of matched Ad
                subAdHash.clear()
                subAdHash = hashes[sb_dt].copy()
                subAdHashList = subAdHash.values()
                subAdHashList = list(subAdHashList)

                adCounter += 1

                for _ in range(1):

                    for _ in range(25):
                        adHsh = subAdHashList[x1]
                        diff = hamming(check, adHsh)
                        x1 += 1
                        if diff <= 5:
                            status = 1
                            active = 1
                            matchAd((x1-1), (t+1), (streamFrameNo-1), diff, sn=1)
                            configLoc = "Ad{} - ({})".format(adNum[t], adName[t])
                            break
                    for _ in range(25):
                        adHsh = subAdHashList[x2]
                        diff = hamming(check, adHsh)
                        x2 += 1
                        if diff <= different:
                            status = 1
                            active = 2
                            matchAd((x2-1), (t+1), (streamFrameNo-1), diff, sn=2)
                            break
                    for _ in range(25):
                        adHsh = subAdHashList[x3]
                        diff = hamming(check, adHsh)
                        x3 += 1
                        if diff <= different:
                            status = 1
                            active = 3
                            matchAd((x3-1), (t+1), (streamFrameNo-1), diff, sn=3)
                            break
                    # for _ in range(10):
                        # adHsh = subAdHashList[x4]
                        # diff = hamming(check, adHsh)
                        # x4 += 1
                        # if diff <= different:
                            # status = 1
                            # active = 4
                            # matchAd((x4-1), (t+1), (streamFrameNo-1), diff, sn=4)
                            # break
                    # for _ in range(10):
                        # adHsh = subAdHashList[x5]
                        # diff = hamming(check, adHsh)
                        # x5 += 1
                        # if diff <= different:
                            # status = 1
                            # active = 5
                            # matchAd((x5-1), (t+1), (streamFrameNo-1), diff, sn=5)
                            # break

        elif status == 1:

            if len(checkDictList) > adFrameNo:  # set limit

                currentHash = checkDictList[st]
                adFrameNo += 1
                st += 1

                dif = hamming(currentHash, check)

                if adFrameNo == len(checkDictList):
                    matchCounterFinal = matchCount
                    missMatchCounterFinal = missMatchCount
                    totalFrameCounter = len(checkDict.keys())
                    endSF = streamFrameNo

                if dif <= different:
                    logger1.info("SF {} - match with AdF ".format(streamFrameNo-1) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + "   [Hash: " + str(check) + ']')
                    print("SF {} - match with AdF ".format(streamFrameNo-1) + str(st) + " - Dif = " +
                          str(dif))

                    if active == 1:
                        sn1 += 1
                    elif active == 2:
                        sn2 += 1
                    elif active == 3:
                        sn3 += 1
                    elif active == 4:
                        sn4 += 1
                    elif active == 5:
                        sn5 += 1

                    matchCount += 1

                elif dif > different:
                    logger1.info("SF {} - miss match with AdF ".format(streamFrameNo-1) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')
                    print("SF {} - miss match with AdF ".format(streamFrameNo-1) + str(st) + " - Dif = " +
                          str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')

                    missMatchCount += 1
                    status = 0

            else:
                # logger1.info("SF {} - no match".format(streamFrameNo-1))
                status = 0

    else:
        break

capture.release()

imgList = list(streamImg.values())

# if totalFrameCounter == 0:
    # logger1.info('-------' * 5)
    # logger1.info("--Not found any match Ad--")

# else:
    # pre = ((totalFrameCounter - missMatchCounterFinal) / totalFrameCounter) * 100

    # logger1.info('-------' * 5)
    # logger1.info('-------' * 5)
    # logger1.info("Total frames of ad = {}".format(totalFrameCounter))
    # logger1.info("Matched frames = {}".format(totalFrameCounter - missMatchCounterFinal))
    # logger1.info("Miss matched frames = {}".format(missMatchCounterFinal))
    # logger1.info("Match percentage : {}%\n\n\n".format(round(pre, 2)))
    # logger3.info("Match percentage of Ad{} ({}): {}%\n\n\n".format((t+1), adName[t], round(pre, 2)))

    # print('-------' * 5)
    # print('-------' * 5)
    # print("Total frames of ad = {}".format(totalFrameCounter))
    # print("Matched frames = {}".format(totalFrameCounter - missMatchCounterFinal))
    # print("Miss matched frames = {}".format(missMatchCounterFinal))
    # print("Match percentage : {}%\n\n\n".format(round(pre, 2)))

mainEnd = time.time()
logger1.info("Total time duration = {} seconds".format(round((mainEnd - mainStart), 2)))
print("Total time duration = {} seconds".format(round((mainEnd - mainStart), 2)))
print("Match frames - sn 1 = {}".format(sn1))
print("Match frames - sn 2 = {}".format(sn2))
print("Match frames - sn 3 = {}".format(sn3))
# print("Match frames - sn 4 = {}".format(sn4))
# print("Match frames - sn 5 = {}".format(sn5))
print("Total match frames count = {}".format(matchCount-1))
print("Total miss match frames count = {}".format(missMatchCount))
matchingPre = (matchCount / 139) * 100
print("Matching percentage = {}%".format(matchingPre))

logger3.info("Match frames - sn 1 = {}".format(sn1))
logger3.info("Match frames - sn 2 = {}".format(sn2))
logger3.info("Match frames - sn 3 = {}".format(sn3))
logger3.info("Total match frames count = {}".format(matchCount-1))
logger3.info("Total miss match frames count = {}".format(missMatchCount))
logger3.info("Matching percentage = {}%".format(matchingPre))

fh = open("E:\\Opencv_project\\Frames\\Set01\\" + str(configLoc) + "\\config.txt", 'w')
fh.write("key frame 1 == {}\n".format(kx1))
fh.write("key frame 2 == {}\n".format(kx2))
fh.write("key frame 3 == {}\n".format(kx3))
# fh.write("key frame 4 == {}\n".format(kx4))
# fh.write("key frame 5 == {}\n".format(kx5))
fh.close()
