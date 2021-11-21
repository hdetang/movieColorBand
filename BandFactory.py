from threading import Thread
import numpy as np
from time import sleep

class BandFactory:

    def __init__(self, maxIndex, frames = {}):
        self.frames = frames
        self.maxIndex = maxIndex
        self.band = np.empty((50, maxIndex + 1, 3))
        self.thread = None

    def start(self):    
        self.thread = Thread(target=self.processFrames)
        self.thread.start()
        return self

    def processFrames(self):
        index = 0
        while True:
            # If we're past the duration of the video, we end the method
            if (index >= self.maxIndex):
                break

            # If frames aren't available, wait a short time before trying again
            if (index not in self.frames):
                sleep(0.02)
                continue

            frame = self.frames[index]

            # Flatten the frame by its colors and get their respective count
            colors, colorsCount = np.unique(frame.reshape(-1, frame.shape[2]), axis=0, return_counts=True)

            # Get the color having the most occurences (making it the most dominant one)
            dominantColor = colors[colorsCount.argmax()]

            # Hydrate one column of pixel in the band with the current frame's dominant color
            self.band[0:50, index] = np.full((1, 50, 3), dominantColor)
            index += 1
