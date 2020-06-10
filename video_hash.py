import cv2
import imutils


def dHash(image):
    resized = cv2.resize(image, (9, 8))
    diff = resized[:, 1:] > resized[:, -1:]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


capture1 = cv2.VideoCapture('img\Megamind.avi');

while (True):
    ret, frame = capture1.read()

    if ret == True:
        cv2.imshow('frame1', frame)

        hashFrame = dHash(frame)
        print(hashFrame)

        hashDict = {}
        update = hashDict.get(hashFrame, [])
        update.append(hashFrame)
        hashDict[hashFrame] = update

        if cv2.waitKey(1) == ord('q'):
            break

    else:
        break

print('###################################################################################')

capture2 = cv2.VideoCapture('img\Megamind.avi');

while (True):
    ret, frame = capture2.read()

    if ret == True:
        cv2.imshow('frame2', frame)

        hashFrame = dHash(frame)
        print(hashFrame)

        matchHash = hashDict.get(hashFrame, [])

        for i in matchHash:
            if hashFrame == matchHash:
                print('Equal videos')

            else:
                print('Different videos')

        if cv2.waitKey(1) == ord('q'):
            break

    else:
        break

print('------------' * 5)
print(hashDict)
capture1.release()
capture2.release()
cv2.destroyAllWindows()
