from constants import *
import cv2
import dataclasses


FRAME_WIDTH_RANGE = (400, 2000)
FRAME_WIDTH_DELTA = 200
FRAME_RATE_RANGE = (10, 60)
FRAME_RATE_DELTA = 10


@dataclasses.dataclass()
class CaptureSetting:
    width: int
    height: int
    frameRates: list[int] = dataclasses.field(default_factory=list)
    def format(self):
        return f'{self.width:.0f}x{self.height:.0f}@' + '/'.join(f'{r:.0f}' for r in self.frameRates)


def main():
    validSettings = []
    capture = cv2.VideoCapture(CAPTURE_SOURCE)

    for width in range(*FRAME_WIDTH_RANGE, FRAME_WIDTH_DELTA):
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        trueWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        trueHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        setting = CaptureSetting(trueWidth, trueHeight)
        if setting not in validSettings:
            validSettings.append(setting)
    
    for setting in validSettings:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, setting.width)
        for rate in range(*FRAME_RATE_RANGE, FRAME_RATE_DELTA):
            capture.set(cv2.CAP_PROP_FPS, rate)
            frameRate = capture.get(cv2.CAP_PROP_FPS)
            if frameRate not in setting.frameRates:
                setting.frameRates.append(frameRate)
    
    print(', '.join(s.format() for s in validSettings))


if __name__ == '__main__':
    main()
