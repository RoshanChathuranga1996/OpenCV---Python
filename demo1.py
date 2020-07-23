import time
import cv2
import numpy as np
import pickle
from imutils import paths
import logging


def dhash(image, hashsize=8):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (hashsize + 1, hashsize))
    diff = resized[:, 1:] > resized[:, -1:]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def convert_hash(h):
    return int(np.array(h, dtype='float64'))


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

            print("Processing Ad" + str(num+1) + " F_No {}".format(frame_no))
            # cv2.imwrite('C:\\Users\\Roshan\\Desktop\\New folder\\FrameWrite\\Ad' + str(num+1) + '_frame ' + str(
            # frame_no) + '.jpg', frames)
            frame_no += 1

            img_encode = cv2.imencode('.jpg', frames)[1]
            data_encode = np.array(img_encode)
            str_encode = data_encode.tostring()

            update = imgSources[one].get(frame_no, [])
            update.append(str_encode)
            imgSources[one][hsh] = update

            d = {frame_no: hsh}
            hashes[one].update(d)

        else:
            break

    end1 = time.time()
    print('Sub dictionary {} updated.'.format(nested_key[num]))
    print('--------' * 7)
    print("[INFO] Loading video took {} seconds".format(end1 - start1))
    print('--------' * 7)

    logging.info('Ad {} loaded\n'.format(num+1) + 'No of frames = ' + str(frame_no) + ' : Time elapsed = ' +
                 str(end1-start1) + ' seconds')

    return hashes, firstFrame


hashes = {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}}
nested_key = list(hashes.keys())
imgSources = {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}}
firstFrame = []
matchedAdFrame = {}
currentHashList = []
loopNo = 0

Log_filename = "C:\\Users\\Roshan\\Desktop\\Intern\\Log\\TxtAdDetection.log"
logging.basicConfig(level=logging.DEBUG, filename=Log_filename, filemode='w',
                    format='%(levelname)s:%(asctime)s:'
                           ' %(message)s', datefmt='%d-%b-%Y - %I:%M:%S %p')

logging.info("<< App Started >> \n")

adFolder = 'C:\\Users\\Roshan\\Downloads\\Video\\Sample'
samplePaths = list(paths.list_files(adFolder, validExts=".mp4"))

logging.info("Loading ad folder : {}".format(adFolder))

# try:
#    list.count() == 0
#
# except Exception as e:
#    logging.error('No video files to read!', exc_info=True)

for (i, samplePath) in enumerate(samplePaths):
    sampleCreate(samplePath, loopNo)
    loopNo += 1

logging.info("\n")
logging.info("Ads loaded successfully")
logging.info('--------' * 7)

print("[INFO] serializing hashes...")
logging.info("[INFO] serializing hashes...")
f = open('C:\\Users\\Roshan\\Desktop\\New folder\\hashes_vid.pickle', 'wb')
f.write(pickle.dumps(hashes))
f.close()

print("[INFO] loading hashes...")
logging.info("[INFO] loading hashes...")
hashes = pickle.loads(open('C:\\Users\\Roshan\\Desktop\\New folder\\hashes_vid.pickle', 'rb').read())

# print(firstFrame)

# masterPath = list(paths.list_files("'C:\\Users\\Roshan\\Downloads\\Video\\Sample\\dolbycanyon.m4v"))
capture = cv2.VideoCapture('vid/Stream_edit.mp4')

# check the try statement.
# try:
#    capture is not open()
#
# except Exception as e:
#    logging.warning('<< Stream not available >>', exc_info=True)

logging.info('--------' * 7)
logging.info("<< Reading video stream... >>")
logging.info('--------' * 7)

print('--------' * 7)
print("<< Reading video stream... >>")
print('--------' * 7)

status = 0
adFrameNo = 1  # 1
streamFrm = 1
fstFrm_Count = len(firstFrame)
matchCount = 1
missMatchCount = 0


while True:
    ret, frame = capture.read()

    if ret:
        check = dhash(frame)
        check = convert_hash(check)
        j = 0
        # cv2.imwrite('C:\\Users\\Roshan\\Desktop\\New folder\\FrameWrite\\Stream_frame ' + str(streamFrm) + '.jpg',
        # frame)
        print('Processing SF_No {}'.format(streamFrm))
        # logging.info('Processing SF_No {}'.format(streamFrm))
        streamFrm += 1

        if status == 0:
            for x in firstFrame:

                if check == x:
                    match = nested_key[j]
                    print("Match to Ad {}...".format(j+1))
                    print("<< Working with Ad {} >>".format(j+1))
                    logging.info('-------' * 5)
                    logging.info("Match to Ad {}...".format(j+1))
                    logging.info("<< Working with Ad {} >>".format(j+1))
                    logging.info('-------' * 5)

                    # get the frames of matched ad
                    matchedAdFrame = hashes[match].copy()
                    currentHashList = matchedAdFrame.values()
                    currentHashList = list(currentHashList)

                    print('Stream hash {}        : '.format(streamFrm-1) + str(check))
                    print('Checking with hash     : ' + str(x))
                    print("Ad frame No            : " + str(adFrameNo))
                    print("[Match found]")
                    print('-------' * 5)
                    logging.info("SF {} - match with AdF ".format(streamFrm-1) + str(adFrameNo))

                    status = 1
                    break

                else:
                    j += 1
                    if fstFrm_Count == j:
                        print("No match found")
                        logging.info("SF {} - no match".format(streamFrm-1))

        elif status == 1:

            if len(currentHashList) > adFrameNo:

                # check with matched ad frames. starting from 2nd frame
                currentHash = currentHashList[adFrameNo]

                print('Stream hash {}        : '.format(streamFrm-1) + str(check))
                print('Checking with hash     : ' + str(currentHash))

                adFrameNo += 1

                if check == currentHash:

                    matchCount += 1
                    print("Ad frame No            : " + str(adFrameNo))
                    print("[Match found]")
                    print('-------' * 5)
                    logging.info("SF {} - match with AdF ".format(streamFrm-1) + str(adFrameNo))

                else:
                    missMatchCount += 1
                    print("[Miss match found !]")
                    print('-------' * 5)
                    logging.info("SF {} - miss match with AdF ".format(streamFrm-1) + str(adFrameNo))

            else:
                status = 0

    else:
        break

capture.release()

print('-------' * 5)
print("Total frames of ad = {}".format(matchCount+missMatchCount))
print("Matched frames = {}".format(matchCount))
print("Miss matched frames = {}".format(missMatchCount))

logging.info('-------' * 5)
logging.info("Total frames of ad = {}".format(matchCount+missMatchCount))
logging.info("Matched frames = {}".format(matchCount))
logging.info("Miss matched frames = {}".format(missMatchCount))

totalF = missMatchCount + matchCount
pre = (matchCount / totalF)*100

print("Match percentage : {}%".format(pre))
logging.info("Match percentage : {}%".format(pre))


