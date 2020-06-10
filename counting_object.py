import cv2
import imutils

image = cv2.imread('img/obj.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
corner = cv2.Canny(gray, 30, 150)
# Thresholding can help us to remove lighter or darker regions and contours of images

thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

for c in cnts:
    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
    cv2.imshow("Contours", output)

text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (240, 0, 159), 2)

mask = thresh.copy()    # reduce the size of foreground objects/ reduce the contour sizes
mask = cv2.erode(mask, None, iterations=5)

mask = thresh.copy()    # To enlarge the regions
mask = cv2.dilate(mask, None, iterations=5)

mask = thresh.copy()
outputx = cv2.bitwise_and(image, image, mask=mask)


cv2.imshow("Output", outputx)
cv2.imshow("Dilated", mask)
cv2.imshow("Eroded", mask)
cv2.imshow("Contours", output)
cv2.imshow('image', image)
cv2.imshow('gray', gray)
cv2.imshow('corner', corner)
cv2.imshow('thresh', thresh)
cv2.waitKey(0)
