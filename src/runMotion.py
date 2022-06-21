from constants import *
import camera
import uploadAll
import cv2
import time
import datetime


def runMotion():
    feed = camera.Camera()
    isCapturing = False
    frame = cv2.cvtColor(feed.read(), cv2.COLOR_BGR2GRAY)

    while True:
        framePrevious = frame
        frame = cv2.cvtColor(feed.read(), cv2.COLOR_BGR2GRAY)
        diff = CAM_CONFIG.diffScale * cv2.norm(frame, framePrevious)
        print(f'{diff:.2f}')

        if diff > DIFF_THRESHOLD and not isCapturing:
            isCapturing = True
            fileName = datetime.datetime.now().strftime('%B %d, %H-%M-%S.avi')
            writer = cv2.VideoWriter(str(ASSETS_DIR / fileName), cv2.VideoWriter_fourcc(*'MJPG'), CAM_CONFIG.frameRate, CAM_CONFIG.cropResolution)
            print(f'started capturing "{fileName}"')
            for _ in range(CAM_CONFIG.captureCount):
                writer.write(feed.read())

        elif diff > DIFF_THRESHOLD and isCapturing:
            for _ in range(CAM_CONFIG.captureCount):
                writer.write(feed.read())

        elif isCapturing:
            isCapturing = False
            writer.release()
            print(f'ended capturing')
            uploadAll.uploadAll()
            print('\n')

        else:
            time.sleep(DETECT_DELAY)


if __name__ == '__main__':
    runMotion()
