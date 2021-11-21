import cv2 as cv
from time import time
import sys    

from VideoFrames import VideoFrames
from BandFactory import BandFactory

def formatExecutionTime(executionTime):
    hours = f'{int(executionTime // 3600):02d}'
    remainingSeconds = executionTime % 3600
    minutes = f'{int(remainingSeconds // 60):02d}'
    remainingSeconds = f'{(remainingSeconds % 60):05.2f}'

    return (hours + 'h ' + minutes + 'm ' + remainingSeconds +'s')

if __name__ == '__main__': 
    # Get the command line arguments
    try:
        path = sys.argv[1]
    except ValueError:
        print('Missing argument: <path>')
        exit()

    startTime = time();

    videoFrames = VideoFrames(path).start()
    bandFactory = BandFactory(videoFrames.duration, videoFrames.frames).start()

    videoFrames.thread.join()
    bandFactory.thread.join()

    # The video is saved as a color band with each second's most dominant color as a column of pixel
    cv.imwrite('./bands/' + videoFrames.fileName + '-band.png', bandFactory.band)

    endTime = time()

    print('Execution time : ', formatExecutionTime(round(endTime - startTime, 2)))
    print('Press any key to leave the image...')

    cv.imshow('band', bandFactory.band)
    cv.waitKey()