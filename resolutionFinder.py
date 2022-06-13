from constants import *
import cv2


def main():
    validResolutions = []
    capture = cv2.VideoCapture(CAPTURE_SOURCE)
    for width in range(*FRAME_WIDTH_RANGE, FRAME_WIDTH_DELTA):
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frameSize = (frameWidth, frameHeight)

        if frameSize not in validResolutions:
            validResolutions.append(frameSize)
    
    print(validResolutions)

if __name__ == '__main__':
    main()
