import numpy as np

def getDominantColor(image, dimensions):
    # Flatten the frame by its colors and get their respective count
    colors, colorsCount = np.unique(image.reshape(-1, dimensions), axis=0, return_counts=True)

    # Get the color having the most occurences (making it the most dominant one)
    countSort = np.argsort(-colorsCount)
    colors = colors[countSort]

    dominantColor = colors[0]

    # Due to lightning, there is a high chance black is the most dominant color in a movie so we skip it to get the second most dominant color
    if np.array_equal(dominantColor, [0,0,0]) and 1 in colors:
        dominantColor = colors[1]

    return dominantColor

def setImageWidth(image, width, height):
    imageHeight, imageWidth, channels = image.shape

    if width > imageWidth: return image

    newImage = np.empty((height, width, 3))

    ratio = imageWidth // width
    offset = imageWidth % width

    start = 0
    end = ratio

    for index in range(width):
        if (offset > index): end += 1

        slice = image[0, start:end]

        dominantColor = getDominantColor(slice, channels)

        # Hydrate one column of pixel in the band with the current frame's dominant color
        newImage[0:height, index] = np.full((1, height, 3), dominantColor)

        start = end
        end += ratio
        if end > imageWidth: end = imageWidth

    return newImage