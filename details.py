import cv2
import numpy as np

img = cv2.imread('img/messi5.jpg')
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', img)

cropimg = img[0:200, 100:300]
cv2.resize(cropimg, (100, 100))
cv2.imshow('crp', cropimg)


print(img.size)
print(img.dtype)
print(img.shape)
print(cropimg.shape)



cv2.waitKey(0)
cv2.destroyAllWindows()