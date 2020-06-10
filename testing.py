from imutils import paths
import time
import cv2
import os


def dhash(image, hashsize=8):
    resized = cv2.resize(image, (hashsize + 1, hashsize))
    diff = resized[:, 1:] > resized[:, -1:]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


print("[INFO] computing hashes for base...")
basePath = list(paths.list_images('C:\\Users\\Roshan\\Desktop\\Intern\\Opencv\\image-hashing-opencv\\haystack'))
checkPath = list(paths.list_images('C:\\Users\\Roshan\\Desktop\\Intern\\Opencv\\image-hashing-opencv\\needles'))

print(basePath)
print(checkPath)

# if sys.platform != "win32":
    # basePath = [bc.replace("\\", "") for bc in basePath]
    # checkPath = [bc.replace("\\", "") for bc in checkPath]

BASE_PATHS = set([bc.split(os.path.sep)[-2] for bc in checkPath])  # base subdirectories for the check paths
base = {}  # dictionary that will map the image hash to corresponding image
start = time.time()  # start the timer

# loop over the base paths
for bc in basePath:

    image = cv2.imread(bc)

    if image is None:
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageHash = dhash(image)
    # print(imageHash)

    # update the base dictionary
    update = base.get(imageHash, [])
    update.append(bc)
    base[imageHash] = update

print("[INFO] processed {} images in {:.2f} seconds".format(
    len(base), time.time() - start))  # time for hashing base images
print("[INFO] computing hashes for check...")

# loop over the check paths
for bc in checkPath:
    image = cv2.imread(bc)

    if image is None:
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageHash = dhash(image)
    print(imageHash)
    # result = cv2.transform(imageHash, )

    matchedPaths = base.get(imageHash, [])  # grab all image paths that match the hash

    # loop over all matched paths
    for matchedPath in matchedPaths:

        x = bc.split(os.path.sep)[-2]  # extract the subdirectory from the image path
        print('Removed :- ' + x)

        if x in BASE_PATHS:  # images, remove it. if it not in base path
            BASE_PATHS.remove(x)

print("[INFO] check the following directories...")

for x in BASE_PATHS:
    print('[INFO] {}'.format(x))

print("Done...")