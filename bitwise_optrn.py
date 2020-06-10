import cv2
import numpy as np

img1 = np.zeros((277, 576, 3), np.uint8)
img1 = cv2.rectangle(img1, (238, 0), (338, 100), (255, 255, 255), -1)
img2 = cv2.imread('img/image_1.jpg')

cv2.imshow('image1', img1)
cv2.imshow('image2', img2)

bitAnd = cv2.bitwise_and(img1, img2)
bitOr = cv2.bitwise_or(img1, img2)
bitXor = cv2.bitwise_xor(img1, img2)
bitNot1 = cv2.bitwise_not(img1)
bitNot2 = cv2.bitwise_not(img2)

#cv2.imshow('and', bitAnd)
#cv2.imshow('or', bitOr)
#cv2.imshow('xor', bitXor)
cv2.imshow('not1', bitNot1)
cv2.imshow('not2', bitNot2)

cv2.waitKey(0)
cv2.destroyAllWindows()