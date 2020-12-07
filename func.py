import cv2
import numpy as np


def dHash(image, hashsize=8):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hashsize + 1, hashsize))
    diffD = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diffD.flatten()) if v])


def convert_hash(h):
    return int(np.array(h, dtype="float64"))


def hammingD(a, b):
    return bin(int(a) ^ int(b)).count("1")


def hamming(a, b):
    string1 = str(a)
    string2 = str(b)
    distance = 0
    lnt = len(string1)

    for y in range(lnt):
        if string1[y] != string2[y]:
            distance += 1

    return distance
