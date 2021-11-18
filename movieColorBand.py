import cv2 as cv
import numpy as np

import sys

# Get the command line arguments
try:
    path = sys.argv[1]
except ValueError:
    print('Missing argument: <path>')
    exit()

# Get the video file
video = cv.VideoCapture(path)

if (video.isOpened() == False):
      print("Error opening the video file")
      exit()

# Get frame count, the frame per seconds and thus calculate the duration of the video
frameCount = int(video.get(cv.CAP_PROP_FRAME_COUNT))
fps = int(video.get(cv.CAP_PROP_FPS))
duration = frameCount // fps

print('Frame count : ', frameCount)
print('FPS : ', fps)
print('Video duration : ', duration, 'seconds')

# Create an empty numpy array that will be the final render
band = np.empty((50, duration + 1, 3))

index = 0
frameIndex = 0

while(video.isOpened()):
    ret, frame = video.read()
    print(index)

    if ret == False:
        break

    # Flatten the frame by its colors and get their respective count
    colors, colorsCount = np.unique(frame.reshape(-1, frame.shape[2]), axis=0, return_counts=True)

    # Get the color having the most occurences (making it the most dominant one)
    dominantColor = colors[colorsCount.argmax()]

    # Hydrate one column of pixel in the band with the current frame's dominant color
    band[0:50, index] = np.full((1, 50, 3), dominantColor)
    
    index += 1
    frameIndex += fps

    # Set the next frame to the next second of the video
    video.set(cv.CAP_PROP_POS_FRAMES, frameIndex)

video.release()
cv.destroyAllWindows()

# The video is saved as a color band with each second's most dominant color as a column of pixel
cv.imwrite('./band.png', band)

print('Press any key to leave the image...')

cv.imshow('band', band)
cv.waitKey()
