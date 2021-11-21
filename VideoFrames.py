from threading import Thread
import cv2 as cv

class VideoFrames:

    def __init__(self, path):
        self.video = cv.VideoCapture(path)
        self.frameCount = int(self.video.get(cv.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.video.get(cv.CAP_PROP_FPS))
        self.duration = self.frameCount // self.fps
        self.frames = {}
        self.frameIndex = -1
        self.thread = None
        self.setFileName(path)

    def start(self):
        print('Frame count : ', self.frameCount)
        print('FPS : ', self.fps)
        print('Video duration : ', self.duration, 'seconds')

        self.thread = Thread(target=self.getFrames)
        self.thread.start()

        return self

    def getFrames(self):
        while(True):
            grabbed = self.video.grab()

            if not grabbed:
                break

            # Get the current position of the video file in milliseconds
            currentFrame = self.video.get(cv.CAP_PROP_POS_MSEC) / 1000
            if int(currentFrame) > int(self.frameIndex):
                # Only retrieve and save the first frame in each new second
                self.frames[int(currentFrame)] = self.video.retrieve()[1]
            self.frameIndex = currentFrame
            
        self.video.release()
        cv.destroyAllWindows()

    def setFileName(self, path):
        fullFileName = path.split('/' if '/' in path else '\\')[-1]
        extension = '.' + fullFileName.split('.')[-1]
        self.fileName = fullFileName.removesuffix(extension)