import pickle
from datetime import datetime
from hashingAd import logger1, logger3, nested_key, adName, hashD
from func import hammingD, hamming
import time
import os

mainStart = time.time()
hashes = pickle.loads(open('E:\\Opencv_project\\Pkl\\hashes.pickle', 'rb').read())
adNum = list(adName.keys())
adName = list(adName.values())

i = 0
subAdHash = {}
subAdHashD = {}
checkDict = {}
checkDictD = {}
streamImg = {}
checkDictList = []
checkDictListD = []
subAdHashList = []
subAdHashListD = []
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
kx1 = 867  # sn 1 - 68f
kx2 = 942  # sn 2 - 30f
kx3 = 972  # sn 3 - 33f
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


def matchAd(fNo, adNo, stNo, di, sn):
    global checkDict, checkDictList, status, streamFld, st, checkDictD, checkDictListD, ff
    st = fNo
    checkDict = subAdHash.copy()
    checkDictList = checkDict.values()
    checkDictList = list(checkDictList)

    checkDictD = subAdHashD.copy()
    checkDictListD = checkDictD.values()
    checkDictListD = list(checkDictListD)

    logger1.info('-------' * 5)
    logger1.info("Match to Ad {}...".format(adNo))

    logger1.info("<< Working with Ad {} ({}) >>".format(adNo, adName[adNo - 1]))
    logger1.info('-------' * 5)
    logger3.info("<< Working with Ad {} ({}) sn {} with stream frame {} & Ad frame {} >>".format(adNo, adName[adNo - 1],
                                                                                                 sn, stNo, fNo))
    logger3.info('-------' * 5)

    logger1.info("SF {} - match with AdF {} - Dif = {}".format(stNo, fNo, di))
    print("SF {} - match with AdF {} - Dif = {}".format(stNo, fNo, di))
    print("Matched with sn {}".format(sn))

    currentDt = datetime.date(datetime.now()).strftime("%Y%b%d")
    currentTm = datetime.time(datetime.now()).strftime("%I-%M-%S %p")
    ff = "AD{} ({}) - {}, {}".format(adNo, adName[adNo - 1], currentDt, currentTm)

    streamFld = r'E:\\Opencv_project\\Frames\\Set01\\Match_frames\\{}'.format(ff)
    if not os.path.exists(streamFld):
        os.makedirs(streamFld)


# Stream
path = "E:\\Opencv_project\\StreamTxt\\Stream.txt"
streamTxt = open(path, "r")
lines = streamTxt.readlines()

for line in lines:

    lineSplit = line.split(sep=" ")

    check = lineSplit[2]
    checkD = lineSplit[3]

    print("Processing frame {}".format(i))

    if status == 0:

        adCounter = 0
        for t in range(len(nested_key)):
            sb_dt = nested_key[t]
            x1 = kx1
            x2 = kx2
            x3 = kx3

            # Get the frames of matched Ad
            subAdHash.clear()
            subAdHash = hashes[sb_dt].copy()
            subAdHashList = subAdHash.values()
            subAdHashList = list(subAdHashList)

            subAdHashD.clear()
            subAdHashD = hashD[sb_dt].copy()
            subAdHashListD = subAdHashD.values()
            subAdHashListD = list(subAdHashListD)

            adCounter += 1

            for _ in range(1):

                for _ in range(25):
                    adHsh = subAdHashList[x1]
                    diff = hamming(check, adHsh)
                    x1 += 1
                    if diff <= 5:
                        status = 1
                        active = 1
                        matchAd((x1 - 1), (t + 1), (streamFrameNo - 1), diff, sn=1)
                        configLoc = "Ad{} - ({})".format(adNum[t], adName[t])
                        break
                for _ in range(25):
                    adHsh = subAdHashList[x2]
                    diff = hamming(check, adHsh)
                    x2 += 1
                    if diff <= different:
                        status = 1
                        active = 2
                        matchAd((x2 - 1), (t + 1), (streamFrameNo - 1), diff, sn=2)
                        break
                for _ in range(25):
                    adHsh = subAdHashList[x3]
                    diff = hamming(check, adHsh)
                    x3 += 1
                    if diff <= different:
                        status = 1
                        active = 3
                        matchAd((x3 - 1), (t + 1), (streamFrameNo - 1), diff, sn=3)
                        break

    elif status == 1:

        if len(checkDictList) > adFrameNo:  # set limit

            currentHash = checkDictList[st]
            currentHashD = checkDictListD[st]
            adFrameNo += 1
            st += 1

            dif = hamming(currentHash, check)
            difD = hammingD(currentHashD, checkD)

            if adFrameNo == len(checkDictList):
                matchCounterFinal = matchCount
                missMatchCounterFinal = missMatchCount
                totalFrameCounter = len(checkDict.keys())
                endSF = streamFrameNo

            if dif <= different:
                logger1.info("SF {} - match with AdF ".format(streamFrameNo - 1) + str(adFrameNo) + " - Dif = " +
                             str(dif) + "   [Hash: " + str(check) + ']')
                print("SF {} - match with AdF ".format(streamFrameNo - 1) + str(st) + " - Dif = " +
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
                if difD <= different:
                    logger1.info(
                        "SF {} - match with AdF ".format(streamFrameNo - 1) + str(adFrameNo) + " - Dif = " +
                        str(dif) + "   [Hash: " + str(check) + ']')
                    print("SF {} - match with AdF ".format(streamFrameNo - 1) + str(st) + " - Dif = " +
                          str(dif))
                    print("D hash diff = {}".format(difD))

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

                else:
                    logger1.info(
                        "SF {} - miss match with AdF ".format(streamFrameNo - 1) + str(adFrameNo) + " - Dif = " +
                        str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')
                    print("SF {} - miss match with AdF ".format(streamFrameNo - 1) + str(st) + " - Dif = " +
                          str(dif) + "   [SH: " + str(check) + ", AH: " + str(currentHash) + ']')
                    print("D hash diff = {}".format(difD))
                    missMatchCount += 1
                    status = 0

        else:
            status = 0
    i += 1


mainEnd = time.time()
logger1.info("Total time duration = {} seconds".format(round((mainEnd - mainStart), 2)))
print("Total time duration = {} seconds".format(round((mainEnd - mainStart), 2)))
print("Match frames - sn 1 = {}".format(sn1))
print("Match frames - sn 2 = {}".format(sn2))
print("Match frames - sn 3 = {}".format(sn3))
print("Total match frames count = {}".format(matchCount - 1))
print("Total miss match frames count = {}".format(missMatchCount))
matchingPre = (matchCount / 139) * 100
print("Matching percentage = {}%".format(matchingPre))

logger3.info("Match frames - sn 1 = {}".format(sn1))
logger3.info("Match frames - sn 2 = {}".format(sn2))
logger3.info("Match frames - sn 3 = {}".format(sn3))
logger3.info("Total match frames count = {}".format(matchCount - 1))
logger3.info("Total miss match frames count = {}".format(missMatchCount))
logger3.info("Matching percentage = {}%".format(matchingPre))

# fh = open("E:\\Opencv_project\\Frames\\Set01\\" + str(configLoc) + "\\config.txt", 'w')
# fh.write("key frame 1 == {}\n".format(kx1))
# fh.write("key frame 2 == {}\n".format(kx2))
# fh.write("key frame 3 == {}\n".format(kx3))
# fh.close()

streamTxt.close()
