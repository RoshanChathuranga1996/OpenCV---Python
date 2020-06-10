from imutils import paths
import time
import cv2
import numpy as np
import pickle
import vptree


def dhash(image, hashsize=8):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (hashsize + 1, hashsize))
    diff = resized[:, 1:] > resized[:, -1:]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def convert_hash(h):
    return int(np.array(h, dtype='float64'))


def hamming(a, b):
    return bin(int(a) ^ int(b)).count('1')


# Index images
imagePaths = list(paths.list_images('C:\\Users\\Roshan\\Desktop\\Intern\\Opencv\\101_ObjectCategories\\airplanes'))
hashes = {}

start = time.time()

for(i, imagePath) in enumerate(imagePaths):

    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    image = cv2.imread(imagePath)

    h = dhash(image)
    h = convert_hash(h)

    update = hashes.get(h, [])
    update.append(imagePath)
    hashes[h] = update

end = time.time()
print('--------' * 7)
print("[INFO] Loading index took {} seconds".format(end - start))

print('--------' * 7)
print("[INFO] building VP-Tree...")
points = list(hashes.keys())
tree = vptree.VPTree(points, hamming)


print("[INFO] serializing VP-Tree...")
f = open('vptree.pickle', 'wb')
f.write(pickle.dumps(tree))
f.close()

print("[INFO] serializing hashes...")
f = open('hashes.pickle', 'wb')
f.write(pickle.dumps(hashes))
f.close()


# Search for image
print("[INFO] loading VP-Tree and hashes...")
tree = pickle.loads(open('vptree.pickle', 'rb').read())
hashes = pickle.loads(open('hashes.pickle', 'rb').read())

searchImg = cv2.imread('img/image_0002.jpg')
cv2.imshow('Search', searchImg)

searchHash = dhash(searchImg)
searchHash = convert_hash(searchHash)
print('Search image hash = ' + str(searchHash))

print('--------' * 7)
print("[INFO] performing search...")
start = time.time()
results = tree.get_all_in_range(searchHash, max_distance=50)
results = sorted(results)
end = time.time()
print("[INFO] search took {} seconds".format(end - start))
print('--------' * 7)

for (d, h) in results:
    resultsPaths = hashes.get(h, [])
    print("[INFO] {} total image(s) with d: {}, h: {}".format(len(resultsPaths), d, h))

    for resultsPath in resultsPaths:
        result = cv2.imread(resultsPath)
        cv2.imshow("Result", result)
        cv2.waitKey(0)