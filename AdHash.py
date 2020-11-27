import cv2
import imagehash
import numpy as np
from PIL import Image
from imutils import paths
import time
import pickle
import logging
import os
from datetime import datetime


hashes = {'A': {}}
imgSources = {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}}
adName = {}
nested_key = list(hashes.keys())
loopNo = 0
timeAdStart = time.time()

# create folders for every day & write logger
currentDt = datetime.date(datetime.now()).strftime("%Y%b%d")
ff = "Logger {}".format(currentDt)
logFld = r'E:\\Opencv_project\\Log\\{}'.format(ff)
if not os.path.exists(logFld):
    os.makedirs(logFld)

# create separate logger
logger1 = logging.getLogger('Info.log')
logger2 = logging.getLogger('Error.log')
logger3 = logging.getLogger('Output.log')

# To override the default severity of logging
logger1.setLevel(logging.INFO)
logger2.setLevel(logging.ERROR)
logger3.setLevel(logging.INFO)

# Set formatter
format_info = '%(levelname)s: %(name)s: %(asctime)s: %(message)s'
format_error = '%(levelname)s: %(name)s: %(asctime)s: %(filename)s : %(message)s'

# Use FileHandler() to log to a file
file_handler_info = logging.FileHandler(logFld + "\\Info.log")
formatter1 = logging.Formatter(format_info, datefmt='%d-%b-%Y - %I:%M:%S %p')
file_handler_info.setFormatter(formatter1)
file_handler_info.suffix = "%Y%b%d - %I:%M:%S %p"

# print to console
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(format_info)


file_handler_error = logging.FileHandler(logFld + "\\Error.log")
# file_handler_error.setLevel(logging.ERROR)
formatter2 = logging.Formatter(format_error, datefmt='%d-%b-%Y - %I:%M:%S %p')
file_handler_error.setFormatter(formatter2)
file_handler_error.suffix = "%Y%b%d - %I:%M:%S %p"

file_handler_output = logging.FileHandler(logFld + "\\Output.log")
file_handler_output.setFormatter(formatter1)
file_handler_output.suffix = "%Y%b%d - %I:%M:%S %p"

# Add the file handler
logger1.addHandler(file_handler_info)
logger2.addHandler(file_handler_error)
logger3.addHandler(file_handler_output)
# logger3.addHandler(stream_handler)

logger1.info("<< App Started >> \n")
logger2.error("<< App Started [ERROR_LOG] >> \n")
logger3.info("<< App Started >> \n")


def sampleCreate(video, num, fName):
    cap = cv2.VideoCapture(video)
    start1 = time.time()
    frame_no = 0

    while True:
        ret1, frames = cap.read()

        if ret1:

            frames = frames[100:400, 0:640]
            # frames = frames[100:490, 0:720]
            # frames = cv2.resize(frames, (640, 300))
            img1 = Image.fromarray(frames)
            hsh = imagehash.phash(img1)
            one = nested_key[num]

            print("Processing Ad" + str(num + 1) + " F_No {} Hash: {}".format(frame_no, hsh))

            adFld = r'E:\\Opencv_project\\Frames\\Set01\\Ad{} - ({})'.format((num + 1), fName)
            if not os.path.exists(adFld):
                os.makedirs(adFld)

            txt_ad = "Hash: {}".format(hsh)
            fnt = cv2.FONT_HERSHEY_SIMPLEX
            frames = cv2.putText(frames, txt_ad, (40, 40), fnt, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imwrite(adFld + "\\" + str(frame_no) + '.jpg', frames)

            d = {frame_no: hsh}
            hashes[one].update(d)

            img_encode = cv2.imencode('.jpg', frames)[1]
            data_encode = np.array(img_encode)
            byt_encode = data_encode.tobytes()

            m = {frame_no: byt_encode}
            imgSources[one].update(m)

            y = {(num + 1): fName}
            adName.update(y)

            frame_no += 1

        else:
            break

    end1 = time.time()

    logger1.info(
        '[ Ad {} loaded ({})] - '.format((num + 1), fName) + 'No of frames = ' + str(frame_no - 1) +
        ' : Time elapsed = ' + str(round((end1 - start1), 2)) + ' seconds')
    logger3.info(
        '[ Ad {} loaded ({})] - '.format((num + 1), fName) + 'No of frames = ' + str(frame_no - 1) +
        ' : Time elapsed = ' + str(round((end1 - start1), 2)) + ' seconds')
    print(
        '[ Ad {} loaded ({})] - '.format((num + 1), fName) + 'No of frames = ' + str(frame_no - 1) +
        ' : Time elapsed = ' + str(round((end1 - start1), 2)) + ' seconds')

    return hashes


# File location of Ad
adFolder = 'E:\\Opencv_project\\Videos\\Ads'
samplePaths = list(paths.list_files(adFolder))

logger1.info("Loading Ad folder : {}".format(adFolder))
logger3.info("Loading Ad folder : {}".format(adFolder))

for (i, samplePath) in enumerate(samplePaths):
    head_tail = os.path.split(samplePath)
    name = head_tail[1]
    sampleCreate(samplePath, loopNo, name)
    loopNo += 1

logger1.info('--------' * 7)
logger1.info("Ads loaded successfully")
logger3.info('--------' * 7)
logger3.info("Ads loaded successfully")

file_h = open('E:\\Opencv_project\\Pkl\\hashes.pickle', 'wb')
file_h.write(pickle.dumps(hashes))
file_h.close()

timeAdEnd = time.time()

logger1.info("Ads hashes created successfully [ Total time duration: {} seconds ] "
             .format(round((timeAdEnd - timeAdStart), 2)))
logger3.info("Ads hashes created successfully [ Total time duration: {} seconds ] "
             .format(round((timeAdEnd - timeAdStart), 2)))
logger1.info('--------' * 7)
logger3.info('--------' * 7)

print('--------' * 7)
print("Created hashes for {} folder".format(adFolder))
