import time
import cv2
import numpy as np
import pickle
import vptree
from imutils import paths
import logging
from matplotlib import pyplot as plt


def dhash(image, hashsize=8):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (hashsize + 1, hashsize))
    diff = resized[:, 1:] > resized[:, -1:]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def convert_hash(h):
    return int(np.array(h, dtype='float64'))


def hamming(a, b):
    return bin(int(a) ^ int(b)).count('1')


def sampleCreate(video, num):

    cap = cv2.VideoCapture(video)
    start1 = time.time()
    frame_no = 1

    while True:
        ret1, frames = cap.read()

        if ret1:
            hsh = dhash(frames)
            hsh = convert_hash(hsh)

            if frame_no == 1:
                firstFrame.append(hsh)

            one = nested_key[num]

            print("Processing Ad" + str(num + 1) + " F_No {}".format(frame_no))

            txt_ad = "Hash = {}".format(hsh)
            fnt = cv2.FONT_HERSHEY_SIMPLEX
            # frames = cv2.putText(frames, txt_ad, (40, 40), fnt, 1, (255, 0, 0), 2, cv2.LINE_AA)
            # cv2.imwrite('C:\\Users\\Roshan\\Desktop\\New folder\\FrameWrite\\Ad{}\\Frame '.format(num+1) +
            # str(frame_no) + '.jpg', frames)

            d = {frame_no: hsh}
            hashes[one].update(d)

            img_encode = cv2.imencode('.jpg', frames)[1]
            data_encode = np.array(img_encode)
            str_encode = data_encode.tostring()

            e = {frame_no: str_encode}
            imgSources[one].update(e)

            frame_no += 1

        else:
            break

    end1 = time.time()
    print('[ Ad {} loaded ]'.format(num + 1))
    print('--------' * 7)
    print("[INFO] Loading video took {} seconds".format(end1 - start1))
    print('--------' * 7)

    logging.info('[ Ad {} loaded ] - '.format(num + 1) + 'No of frames = ' + str(frame_no) + ' : Time elapsed = ' +
                 str(end1 - start1) + ' seconds')

    return hashes, firstFrame


def vpTree(adNo):
    points = list(hashes[adNo].keys())
    tree = vptree.VPTree(points, hamming)

    file_t = open('C:\\Users\\Roshan\\Desktop\\New folder\\vptree_fldImg.pickle', 'wb')
    file_t.write(pickle.dumps(tree))
    file_t.close()

    logging.info("VP-Tree created & loaded")
    tree = pickle.loads(open('C:\\Users\\Roshan\\Desktop\\New folder\\vptree_fldImg.pickle', 'rb').read())
    return tree


hashes = {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}}
nested_key = list(hashes.keys())
imgSources = {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}}
firstFrame = []
matchedAdFrame = {}
currentHashList = []
loopNo = 0

log_format = '%(levelname)s: %(name)s: %(asctime)s: %(message)s'
log_filename = "C:\\Users\\Roshan\\Desktop\\Intern\\Log\\Info.log"
logging.basicConfig(level=logging.INFO, filename=log_filename, filemode='w',
                    format=log_format, datefmt='%d-%b-%Y - %I:%M:%S %p')

logging.info("<< App Started [INFO_LOG] >> \n")

# File location of Ad
adFolder = 'C:\\Users\\Roshan\\Downloads\\Video\\Sample\\Ad'
samplePaths = list(paths.list_files(adFolder, validExts=".mp4"))

logging.info("Loading ad folder : {}".format(adFolder))


for (i, samplePath) in enumerate(samplePaths):
    sampleCreate(samplePath, loopNo)
    loopNo += 1

logging.info("Ads loaded successfully")
logging.info('--------' * 7)

print("[INFO] serializing hashes...")
logging.info("[INFO] serializing hashes...")
file_h = open('C:\\Users\\Roshan\\Desktop\\New folder\\hashes_vid.pickle', 'wb')
file_h.write(pickle.dumps(hashes))
file_h.close()

print("[INFO] loading hashes...")
logging.info("[INFO] loading hashes...")
hashes = pickle.loads(open('C:\\Users\\Roshan\\Desktop\\New folder\\hashes_vid.pickle', 'rb').read())

# Stream
capture = cv2.VideoCapture('vid/Stream.mp4')

logging.info('--------' * 7)
logging.info("<< Reading video stream... >>\n")

print('--------' * 7)
print("<< Reading video stream... >>")
print('--------' * 7)

fstFrm_Count = len(firstFrame)
status = 0
adFrameNo = 1
streamFrm = 1
matchCount = 1
missMatchCount = 0

while True:
    ret, frame = capture.read()

    if ret:
        check = dhash(frame)
        check = convert_hash(check)
        j = 0

        txtAd = "Hash = {}".format(check)
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(frame, txtAd, (40, 40), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imwrite('C:\\Users\\Roshan\\Desktop\\New folder\\FrameWrite\\Stream\\Frame ' + str(streamFrm) + '.jpg', frame)

        print('Processing SF_No {}'.format(streamFrm))
        streamFrm += 1

        if status == 0:
            for x in firstFrame:

                if x == check:
                    match = nested_key[j]
                    print("Match to Ad {}...".format(j + 1))
                    print("<< Working with Ad {} >>".format(j + 1))

                    logging.info('-------' * 5)
                    logging.info("Match to Ad {}...".format(j + 1))

                    vpTree(match)  # No use in this yet

                    logging.info("<< Working with Ad {} >>".format(j + 1))
                    logging.info('-------' * 5)

                    # Get the frames of matched Ad
                    matchedAdFrame = hashes[match].copy()
                    currentHashList = matchedAdFrame.values()
                    currentHashList = list(currentHashList)

                    print('Stream hash {}        : '.format(streamFrm - 1) + str(check))
                    print('Checking with hash     : ' + str(x))
                    print("Ad frame No            : 1")
                    print("[Match found]")
                    print('-------' * 5)

                    logging.info("SF {} - match with AdF 1".format(streamFrm - 1) + " SF H:" + str(check) + " AdF H:" +
                                 str(x))
                    status = 1

                    break

                else:
                    j += 1
                    if fstFrm_Count == j:
                        print("No match found")
                        logging.info("SF {} - no match".format(streamFrm - 1))

        elif status == 1:

            if len(currentHashList) > adFrameNo:

                # check with matched ad frames. starting from 2nd frame
                currentHash = currentHashList[adFrameNo-2]                # 2 diff

                print('Stream hash {}        : '.format(streamFrm - 1) + str(check))
                print('Checking with hash     : ' + str(currentHash))

                adFrameNo += 1

                dif = hamming(check, currentHash)
                print("<< {} >>".format(dif))

                if dif <= 2:

                    matchCount += 1
                    print("Ad frame No            : " + str(adFrameNo))
                    print("[Match found]")
                    print('-------' * 5)
                    logging.info("SF {} - match with AdF ".format(streamFrm - 1) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + " SF H:" + str(check) + " AdF H:" + str(currentHash))

                else:
                    missMatchCount += 1
                    print("[Miss match found !]")
                    print('-------' * 5)
                    logging.info("SF {} - miss match with AdF ".format(streamFrm - 1) + str(adFrameNo) + " - Dif = " +
                                 str(dif) + " SF H:" + str(check) + " AdF H:" + str(currentHash))

                    cv2.namedWindow("StreamFrame", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("StreamFrame", 650, 400)
                    cv2.imshow("StreamFrame", frame)

                    matchDc = nested_key[j]
                    matchDc = str(matchDc)
                    imgLoc = imgSources[matchDc][adFrameNo-1]   # ad frame = 2

                    reImage = np.asarray(bytearray(imgLoc), dtype="uint8")
                    reImage = cv2.imdecode(reImage, cv2.IMREAD_COLOR)

                    plt.figure(figsize=(10, 6))
                    plt.title("Ad frame_{}, Dif : ".format(streamFrm-1) + str(dif))
                    plt.imshow(cv2.cvtColor(reImage, cv2.COLOR_BGR2RGB))
                    plt.show()

            else:
                logging.info("SF {} - no match".format(streamFrm - 1))
                status = 0

    else:
        break

capture.release()

print('-------' * 5)
print("Total frames of ad = {}".format(matchCount + missMatchCount))
print("Matched frames = {}".format(matchCount))
print("Miss matched frames = {}".format(missMatchCount))

logging.info('-------' * 5)
logging.info("Total frames of ad = {}".format(matchCount + missMatchCount))
logging.info("Matched frames = {}".format(matchCount))
logging.info("Miss matched frames = {}".format(missMatchCount))

totalF = missMatchCount + matchCount
pre = (matchCount / totalF) * 100

print("Match percentage : {}%".format(pre))
logging.info("Match percentage : {}%".format(pre))
