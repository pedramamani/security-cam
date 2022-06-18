from constants import *
import cv2


class Camera:
    def __init__(self, config: CameraConfig):
        self.config = config
        if config.isPiCamera:
            import picamera
            import picamera.array
            self.camera = picamera.PiCamera(resolution=config.resolution, framerate=config.frameRate, sensor_mode=config.mode)
            self.camera.rotation = 180
            self.capture = picamera.array.PiRGBArray(self.camera, size=config.resolution)
        else:
            self.camera = cv2.VideoCapture(config.mode)
            assert self.camera.isOpened(), f'failed to open capture {config.mode}'
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.resolution[1])
            self.camera.set(cv2.CAP_PROP_FPS, config.frameRate)
    
    def read(self):
        if self.config.isPiCamera:
            frame = next(self.camera.capture_continuous(self.capture, format='bgr', use_video_port=True)).array
            self.capture.truncate(0)
        else:
            success, frame = self.camera.read()
            assert success, f'frame cannot be read from capture {self.config.mode}'
        frame = frame[self.config.cropStart[1]: self.config.cropEnd[1], self.config.cropStart[0]: self.config.cropEnd[0]]
        return frame
    
    def release(self):
        if not self.config.isPiCamera:
            self.camera.release()


def test():
    import time
    import matplotlib.pyplot as plt

    camera = Camera(MAIN_CONFIG)
    cv2.imshow('camera feed', camera.read())  # initialize camera and window so they don't affect frame capture timing
    captureTimes = [0]
    startTime = time.time()

    while cv2.waitKey(1) == -1:
        cv2.imshow('camera feed', camera.read())
        captureTimes.append(time.time() - startTime)
    camera.release()
    cv2.destroyAllWindows()

    captureIntervals = [(t - captureTimes[i]) * 1000 for i, t in enumerate(captureTimes[1:])]
    plt.plot(captureIntervals)
    plt.plot([0, len(captureIntervals)], [1000 / MAIN_CONFIG.frameRate] * 2)
    plt.xlabel('frame number')
    plt.ylabel('capture time (ms)')
    plt.autoscale(tight=True)
    plt.show()


if __name__ == '__main__':
    test()
