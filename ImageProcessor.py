from email.mime import image
import numpy as np
import cv2 as cv

def resizeImage(image, scale):
    imageHeigth, imageWidth, _ = image.shape

    width = int(imageWidth * scale / 100)
    height = int(imageHeigth * scale / 100)

    return cv.resize(image, (width, height))

def getDominantColor(image):
    pixels = np.float32(image.reshape(-1, 3))

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv.kmeans(pixels, 1, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    return palette[np.argmax(counts)]

def extendImage(image, imageWidth, height, width):
    newImage = np.empty((height, width, 3))

    ratio = width // imageWidth
    
    start = 0
    end = ratio

    for index in range(imageWidth): 
        newImage[0:height, start:end] = np.full((height, ratio, 3), image[0, index])

        start = end
        end += ratio

    return newImage

def reduceImage(image, imageWidth, height, width):
    newImage = np.empty((height, width, 3))

    ratio = imageWidth // width
    offset = imageWidth % width

    start = 0
    end = ratio

    for index in range(width):
        if (offset > index): end += 1

        slice = image[0, start:end]

        if len(slice) == 0: continue
    
        dominantColor = getDominantColor(slice)

        # Hydrate one column of pixel in the band with the current frame's dominant color
        newImage[0:height, index] = np.full((1, height, 3), dominantColor)

        start = end
        end += ratio
        if end > imageWidth: end = imageWidth

    return newImage

def setImageWidth(image, width, height):
    imageWidth = image.shape[1]

    if width > imageWidth: return extendImage(image, imageWidth, height, width)

    return reduceImage(image, imageWidth, height, width)