import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('../Features/img/box.png')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.imread('../Features/img/box_in_scene.png')
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Initiate SIFT
sift = cv2.xfeatures2d.SIFT_create()

# keypoints
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)


bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

good = []
for m, n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])


img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

plt.imshow(img3)
plt.show()
