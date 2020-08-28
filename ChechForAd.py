import cv2
import imagehash
import pickle
from PIL import Image
from AdHash import logger1, logger3, nested_key
import time
import threading
mainStart = time.time()
hashes = pickle.loads(open('E:\\Opencv_project\\Pkl\\hashes.pickle', 'rb').read())

subAdHash = {}
checkDict = {}
streamHashDict = {}
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
sCount = 1


def hamming(a, b):
    string1 = str(a)
    string2 = str(b)
    distance = 0
    lnt = len(string1)

    for y in range(lnt):
        if string1[y] != string2[y]:
            distance += 1
    return distance


def streamHash(capt, FrameNo):
    while True:
        ret, frame = capt.read()

        if ret:
            frame = frame[200:900, 0:1920]
            img2 = Image.fromarray(frame)
            check = imagehash.phash(img2)

            d = {FrameNo: check}
            streamHashDict.update(d)

            print("-- Processing frame {} --".format(FrameNo + 1))

            # txtAd = "Hash = {}".format(check)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # frame = cv2.putText(frame, txtAd, (40, 40), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.imwrite('E:\\Opencv_project\\Frames\\SetAD\\Stream\\Frame ' + str(streamFrameNo) + '.jpg', frame)

            FrameNo += 1
        else:
            break
    capt.release()


def checkForAd(stt):
    global subAdHash, subAdHashList, checkDict, checkDictList, sCount, status
    if stt == 0:

        sCount = 1

        for check in streamHashDict.values():
            adCounter = 0
            print("Check for SF {}".format(sCount))

            for t in range(len(nested_key)):
                sb_dt = nested_key[t]
                # Get the frames of matched Ad
                subAdHash.clear()
                subAdHash = hashes[sb_dt].copy()
                subAdHashList = subAdHash.values()
                subAdHashList = list(subAdHashList)

                adCounter += 1

                for x in range(30):
                    subFrame = subAdHashList[x]

                    if check == subFrame:
                        checkDict = subAdHash.copy()
                        checkDictList = checkDict.values()
                        checkDictList = list(checkDictList)

                        logger1.info('-------' * 5)
                        logger1.info("Matched to Ad {} with stream frame No {}...".format((t + 1), sCount))
                        logger3.info('-------' * 5)
                        logger3.info("Match to Ad {}...".format(t + 1))
                        print('-------' * 5)
                        print("Matched to Ad {} with stream frame No {}...".format((t + 1), sCount))

                        logger1.info("<< Working with Ad {} >>".format(t + 1))
                        logger1.info('-------' * 5)
                        logger3.info("<< Working with Ad {} >>".format(t + 1))
                        logger3.info('-------' * 5)
                        print("<< Working with Ad {} >>".format(t + 1))
                        print('-------' * 5)

                        stt = 1
                        checkWithAd(stt)

                        return checkDict, checkDictList, sCount

                if adCounter == 4:
                    print(" No match ")
            sCount += 1


def checkWithAd(stt):
    global matchCount, missMatchCount, totalFrameCounter, missMatchCounterFinal, matchCounterFinal,\
        adFrameNo, sCount, status
    if stt == 1:

        streamHashList = list(streamHashDict.values())
        for _ in checkDictList:

            if len(checkDictList) >= adFrameNo:
                # check with matched ad frames. starting from 2nd frame
                currentHash = checkDictList[adFrameNo-1]
                check = streamHashList[sCount-1]

                dif = hamming(currentHash, check)

                if dif < 2:
                    logger1.info("SF {} - match with AdF ".format(sCount) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + "   [Hash: " + str(check) + ']')
                    print("SF {} - match with AdF ".format(sCount) + str(adFrameNo) + " - Dif = " +
                          str(dif) + "   [Hash: " + str(check) + ']')

                    matchCount += 1

                    if adFrameNo == len(checkDictList):
                        matchCounterFinal = matchCount
                        missMatchCounterFinal = missMatchCount
                        totalFrameCounter = len(checkDict.keys())
                        stt = 0

                elif adFrameNo == 30:
                    if missMatchCount > 25:
                        print("-- This Ad not match to stream --")
                        stt = 0

                elif dif >= 2:
                    logger1.info("SF {} - miss match with AdF ".format(sCount) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')
                    print("SF {} - miss match with AdF ".format(sCount) + str(adFrameNo) + " - Dif = " +
                          str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')

                    missMatchCount += 1

                    if adFrameNo == len(checkDictList):
                        matchCounterFinal = matchCount
                        missMatchCounterFinal = missMatchCount
                        totalFrameCounter = len(checkDict.keys())
                        stt = 0

            adFrameNo += 1
            sCount += 1

    else:
        logger1.info("SF {} - no match".format(sCount))
        sCount += 1

    return matchCounterFinal, missMatchCounterFinal, totalFrameCounter, stt, sCount


# Stream
path = "C:\\Users\\rosha\\Videos\\Sample\\Stream\\Stream[test01].mp4"
capture = cv2.VideoCapture(path)

# streamHash(capture, streamFrameNo)
# checkForAd(status)

t1 = threading.Thread(target=streamHash(capture, streamFrameNo))
t2 = threading.Thread(target=checkForAd(status))
t1.start()
t2.start()
t1.join()
t2.join()

if totalFrameCounter == 0:
    logger1.info('-------' * 5)
    logger1.info("--Not found any match Ad--")

pre = ((totalFrameCounter - missMatchCounterFinal) / totalFrameCounter) * 100

logger1.info('-------' * 5)
logger1.info("Total frames of ad = {}".format(totalFrameCounter))
logger1.info("Matched frames = {}".format(totalFrameCounter - missMatchCounterFinal))
logger1.info("Miss matched frames = {}".format(missMatchCounterFinal))
logger1.info("Match percentage : {}%\n\n\n".format(round(pre, 2)))
logger3.info("Match percentage : {}%\n\n\n".format(round(pre, 2)))

mainEnd = time.time()
print("Total time duration = {} seconds".format(mainEnd - mainStart))


