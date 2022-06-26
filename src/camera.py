from constants import *
import time
import cv2


class Camera:
    def __init__(self):
        if CAM_CONFIG.isPiCamera:
            import picamera
            import picamera.array
            self.camera = picamera.PiCamera(resolution=CAM_CONFIG.resolution, framerate=CAM_CONFIG.frameRate, sensor_mode=CAM_CONFIG.mode)
            self.camera.rotation = 180
            self.capture = picamera.array.PiRGBArray(self.camera, size=CAM_CONFIG.resolution)
        else:
            self.camera = cv2.VideoCapture(CAM_CONFIG.mode)
            assert self.camera.isOpened(), f'failed to open capture {CAM_CONFIG.mode}'
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_CONFIG.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_CONFIG.resolution[1])
            self.camera.set(cv2.CAP_PROP_FPS, CAM_CONFIG.frameRate)
            self.camera.set(cv2.CAP_PROP_EXPOSURE, 0.3)
            self.camera.set(cv2.CAP_PROP_GAIN, 0.2)
        time.sleep(WARMUP_DELAY)
    
    def read(self):
        if CAM_CONFIG.isPiCamera:
            frame = next(self.camera.capture_continuous(self.capture, format='bgr', use_video_port=True)).array
            self.capture.truncate(0)
        else:
            success, frame = self.camera.read()
            assert success, f'frame cannot be read from capture {CAM_CONFIG.mode}'
            if CAM_CONFIG.rotated:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame = frame[CAM_CONFIG.cropStart[1]: CAM_CONFIG.cropEnd[1], CAM_CONFIG.cropStart[0]: CAM_CONFIG.cropEnd[0]]
        return frame
    
    def release(self):
        if not CAM_CONFIG.isPiCamera:
            self.camera.release()
