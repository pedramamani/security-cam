from constants import *
import camera
import cv2
import time
import matplotlib.pyplot as plt


def testCamera():
    feed = camera.Camera()
    cv2.imshow('feed', feed.read())  # initialize camera and window so they don't affect frame capture timing
    captureTimes = [0]
    startTime = time.time()

    while cv2.waitKey(1) == -1:
        cv2.imshow('feed', feed.read())
        captureTimes.append(time.time() - startTime)
    feed.release()
    cv2.destroyAllWindows()

    captureIntervals = [(t - captureTimes[i]) * 1000 for i, t in enumerate(captureTimes[1:])]
    plt.plot(captureIntervals)
    plt.plot([0, len(captureIntervals)], [1000 / CAM_CONFIG.frameRate] * 2)
    plt.xlabel('frame number')
    plt.ylabel('capture time (ms)')
    plt.autoscale(tight=True)
    plt.show()


if __name__ == '__main__':
    testCamera()
