from constants import *
import camera
import cv2


def saveBackground():
    feed = camera.Camera()
    background = cv2.cvtColor(feed.read(), cv2.COLOR_BGR2GRAY)

    for index in range(1, CAM_CONFIG.captureCount):
        frame = cv2.cvtColor(feed.read(), cv2.COLOR_BGR2GRAY)
        alpha = 1.0 / index
        beta = 1 - alpha
        background = cv2.addWeighted(frame, alpha, background, beta, 0.0)

    cv2.imwrite(str(BACKGROUND_FILE), background)


if __name__ == '__main__':
    saveBackground()
