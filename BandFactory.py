from threading import Thread
import numpy as np
from time import sleep
from ImageProcessor import getDominantColor

class BandFactory:

    def __init__(self, maxIndex, frames = {}):
        self.frames = frames
        self.maxIndex = maxIndex
        self.band = np.empty((1, maxIndex + 1, 3))
        self.thread = None

    def start(self):    
        self.thread = Thread(target=self.processFrames)
        self.thread.start()
        return self

    def processFrames(self):
        index = 0

        while True:
            print('index: ', index)

            # If we're past the duration of the video, we end the method
            if (index >= self.maxIndex):
                break

            # If frames aren't available, wait a short time before trying again
            if (index not in self.frames):
                sleep(0.02)
                continue

            frame = self.frames[index]

            dominantColor = getDominantColor(frame, frame.shape[2])

            # Hydrate one column of pixel in the band with the current frame's dominant color
            self.band[0, index] = np.full((1, 1, 3), dominantColor)

            del self.frames[index]
            index += 1
