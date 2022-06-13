from pkg_resources import SOURCE_DIST
from constants import *
import cv2
import platform
import datetime



def main():
    capture = cv2.VideoCapture(CAPTURE_SOURCE)
    assert capture.isOpened(), f'failed to open capture {CAPTURE_SOURCE}'
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_RESOLUTION[0])
    writer = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'MJPG'), FPS, CAPTURE_RESOLUTION)

    fromTime = datetime.datetime.now()
    frameCount = 0

    while capture.isOpened() and frameCount < 100:
        success, frame = capture.read()
        if success:
            writer.write(frame)
            frameCount += 1
        else:
            break
        cv2.waitKey(1000 // FPS)
    
    toTime = datetime.datetime.now()
    print(f'from {fromTime} to {toTime} - video length {toTime - fromTime}')

    capture.release()
    writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
