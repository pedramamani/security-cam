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
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
            self.camera.set(cv2.CAP_PROP_FPS, FRAME_RATE)
        elif platform.system() == OS.raspbian:
            import picamera
            self.camera = picamera.PiCamera()
            self.camera.resolution = RESOLUTION
            self.camera.framerate = FRAME_RATE
            self.capture = picamera.array.PiRGBArray(self.camera, size=RESOLUTION)
        else:
            assert False, f'{platform.system()} operating system is not supported'
        time.sleep(0.2)  # allow camera to warm up
    
    def read(self):
        if platform.system() == OS.windows:
            success, frame = self.camera.read()
            assert success, f'frame cannot be read from capture {CAPTURE_SOURCE}'
            return frame
        elif platform.system() == OS.raspbian:
            output = self.camera.capture_continuous(self.capture, format='bgr', use_video_port=True)[0]
            self.capture.truncate(0)
            return output.array
    
    def release(self):
        if platform.system() == OS.windows:
            self.camera.release()
        elif platform.system() == OS.raspbian:
            pass


def main():
    camera = Camera()
    writer = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'MJPG'), FRAME_RATE, RESOLUTION)
    fromTime = datetime.datetime.now()
    frameCount = 0

    while frameCount < 100:
        frame = camera.read()
        writer.write(frame)
        frameCount += 1
        cv2.waitKey(1000 // FRAME_RATE)
    
    toTime = datetime.datetime.now()
    duration = toTime - fromTime
    print(f'Start and end times: {fromTime.time()} - {toTime.time()}')
    print(f'Video duration: {duration.total_seconds()}')
    writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
