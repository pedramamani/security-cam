from constants import *
import cv2
import platform
import datetime
import time



class Camera():
    def __init__(self):
        if platform.system() == OS.windows:
            self.camera = cv2.VideoCapture(CAPTURE_SOURCE)
            assert self.camera.isOpened(), f'failed to open capture {CAPTURE_SOURCE}'
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, SETTING.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, SETTING.resolution[1])
            self.camera.set(cv2.CAP_PROP_FPS, SETTING.frameRate)
        elif platform.system() == OS.raspbian:
            import picamera
            import picamera.array
            self.camera = picamera.PiCamera()
            self.camera.resolution = SETTING.resolution
            self.camera.framerate = SETTING.frameRate
            self.camera.rotation = 180
            self.capture = picamera.array.PiRGBArray(self.camera, size=SETTING.resolution)
        else:
            assert False, f'{platform.system()} operating system is not supported'
        time.sleep(1)  # allow camera to warm up
    
    def read(self):
        if platform.system() == OS.windows:
            success, frame = self.camera.read()
            assert success, f'frame cannot be read from capture {CAPTURE_SOURCE}'
            return frame
        elif platform.system() == OS.raspbian:
            output = next(self.camera.capture_continuous(self.capture, format='bgr', use_video_port=True))
            self.capture.truncate(0)
            return output.array
    
    def release(self):
        if platform.system() == OS.windows:
            self.camera.release()
        elif platform.system() == OS.raspbian:
            pass


def main():
    camera = Camera()
    writer = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'MJPG'), SETTING.frameRate, SETTING.resolution)
    fromTime = datetime.datetime.now()
    frameCount = 0

    while frameCount < SETTING.duration * SETTING.frameRate:
        frame = camera.read()
        writer.write(frame)
        frameCount += 1
        if platform.system() == OS.windows:
            cv2.waitKey(CAPTURE_DELAY)
    
    toTime = datetime.datetime.now()
    duration = toTime - fromTime
    print(f'Start time: {fromTime.time()}')
    print(f'Video duration: {duration.total_seconds()}')
    writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
