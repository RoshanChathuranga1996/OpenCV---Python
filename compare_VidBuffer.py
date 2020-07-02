import time
import cv2
import numpy as np
import pickle
import vptree
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


capture = cv2.VideoCapture("vid/dolbycanyon.m4v")
start = time.time()
hashes = {}
i = 0

while True:
    ret, frame = capture.read()

    if ret:

        h = dhash(frame)
        h = convert_hash(h)

        print("Processing Frame_{}".format(str(i)))
        i += 1

        img_encode = cv2.imencode('.jpg', frame)[1]
        data_encode = np.array(img_encode)
        str_encode = data_encode.tostring()

        update = hashes.get(h, [])
        update.append(str_encode)
        hashes[h] = update

    else:
        break

capture.release()

end = time.time()
print('--------' * 7)
print("[INFO] Loading video took {} seconds".format(end - start))

print('--------' * 7)
print("[INFO] building VP-Tree...")
points = list(hashes.keys())
tree = vptree.VPTree(points, hamming)

print("[INFO] serializing VP-Tree...")
f = open('C:\\Users\\Roshan\\Desktop\\New folder\\vptree_vid.pickle', 'wb')
f.write(pickle.dumps(tree))
f.close()

print("[INFO] serializing hashes...")
f = open('C:\\Users\\Roshan\\Desktop\\New folder\\hashes_vid.pickle', 'wb')
f.write(pickle.dumps(hashes))
f.close()


# Search for image
print("[INFO] loading VP-Tree and hashes...")
tree = pickle.loads(open('C:\\Users\\Roshan\\Desktop\\New folder\\vptree_vid.pickle', 'rb').read())
hashes = pickle.loads(open('C:\\Users\\Roshan\\Desktop\\New folder\\hashes_vid.pickle', 'rb').read())


capture2 = cv2.VideoCapture('vid/ezgif.com-video-cutter.m4v')

while True:
    ret, frame2 = capture2.read()

    if ret:

        h2 = dhash(frame2)
        h2 = convert_hash(h2)

        print('--------' * 7)
        print("[INFO] performing search...")
        start = time.time()

        results = tree.get_all_in_range(h2, max_distance=5)
        results = sorted(results)

        for (d, h) in results:
            start = time.time()
            resultsPaths = hashes.get(h, [])
            print("[INFO] {} total image(s) with d: {}, h: {}".format(len(resultsPaths), d, h))

            for resultsPath in resultsPaths:
                if d < 2:

                    reImage = np.asarray(bytearray(resultsPath), dtype="uint8")
                    reImage = cv2.imdecode(reImage, cv2.IMREAD_COLOR)
                    txt = "Difference: {},    ImageHash: {}".format(d, h)

                    cv2.namedWindow("SampleImg", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("SampleImg", 550, 400)
                    cv2.imshow("SampleImg", frame2)

                    plt.figure(figsize=(10, 6))
                    plt.title(txt)
                    plt.imshow(cv2.cvtColor(reImage, cv2.COLOR_BGR2RGB))
                    plt.show()

        end = time.time()
        print("[INFO] Search took {} seconds".format(end - start))

    else:
        break

capture2.release()




