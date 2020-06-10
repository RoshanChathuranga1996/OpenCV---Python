import cv2
import numpy as np
import imutils


def dHash(image):
    resized = cv2.resize(image, (9, 8))
    diff = resized[:, 1:] > resized[:, -1:]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


image1 = cv2.imread('img/joker.jpg')
sized = imutils.resize(image1, width=400)
cv2.imshow('image1', sized)
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
hash1 = dHash(image1)
print('Image 1 hash = ' + str(hash1))


image2 = cv2.imread('img/joker_BW.jpg')
sized = imutils.resize(image2, width=400)
cv2.imshow('image2', sized)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
hash2 = dHash(image2)
print('Image 2 hash = ' + str(hash2))


if hash1 == hash2:
    print('---------------------------')
    print('Same images')
    print('---------------------------')

else:
    print('---------------------------')
    print('Different images')
    print('---------------------------')


cv2.waitKey(0)
cv2.destroyAllWindows()