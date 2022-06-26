from constants import *
import cv2
import dataclasses


FRAME_WIDTH_RANGE = (400, 2000, 200)
FRAME_RATE_RANGE = (10, 60, 10)


@dataclasses.dataclass()
class CaptureConfig:
    width: int
    height: int
    frameRates: list[int] = dataclasses.field(default_factory=list)

    def format(self):
        return f'{self.width:.0f}x{self.height:.0f}@' + '/'.join(f'{r:.0f}' for r in self.frameRates)


def findCameraConfigs():
    validConfigs = []
    capture = cv2.VideoCapture(CAM_CONFIG.mode)

    for width in range(*FRAME_WIDTH_RANGE):
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        trueWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        trueHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        config = CaptureConfig(trueWidth, trueHeight)
        if config not in validConfigs:
            validConfigs.append(config)
    
    for config in validConfigs:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        for frameRate in range(*FRAME_RATE_RANGE):
            capture.set(cv2.CAP_PROP_FPS, frameRate)
            trueFrameRate = capture.get(cv2.CAP_PROP_FPS)
            if trueFrameRate not in config.frameRates:
                config.frameRates.append(trueFrameRate)
    
    print(', '.join(s.format() for s in validConfigs))


if __name__ == '__main__':
    findCameraConfigs()
