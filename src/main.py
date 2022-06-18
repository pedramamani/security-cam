from constants import *
import cv2
import time
import datetime
import os
import numpy as np
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


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
        time.sleep(DETECT_DELAY)  # wait for camera to warm up and adjust
    
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

def setup():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())


def main():
    camera = Camera(MAIN_CONFIG)
    isCapturing = False
    gFrame = cv2.cvtColor(camera.read(), cv2.COLOR_BGR2GRAY)
    
    while True:
        gFramePrev = gFrame
        gFrame = cv2.cvtColor(camera.read(), cv2.COLOR_BGR2GRAY)
        gNorm = cv2.norm(gFrame, gFramePrev) / np.sqrt(MAIN_CONFIG.resolution[0] * MAIN_CONFIG.resolution[1])

        if gNorm > GNORM_THRESHOLD and not isCapturing:
            isCapturing = True
            fileName = datetime.datetime.now().strftime('%B %d, %H-%M-%S.avi')
            writer = cv2.VideoWriter(str(ASSETS_DIR / fileName), cv2.VideoWriter_fourcc(*'MJPG'), MAIN_CONFIG.frameRate, MAIN_CONFIG.cropResolution)
            print(f'started capturing "{fileName}"')

            for _ in range(CAPTURE_COUNT):
                writer.write(camera.read())

        elif gNorm > GNORM_THRESHOLD and isCapturing:
            for _ in range(CAPTURE_COUNT):
                writer.write(camera.read())

        elif isCapturing:
            isCapturing = False
            writer.release()
            print(f'ended capturing "{fileName}"')

            service = build('drive', 'v3', credentials=Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES))
            metadata = {'name': fileName, 'parents': [DRIVE_FOLDER_ID]}
            media = MediaFileUpload(ASSETS_DIR / fileName)
            service.files().create(body=metadata, media_body=media, fields='id').execute()
            del media  # to release the file handle so we can delete it
            os.remove(ASSETS_DIR / fileName)
            print(f'uploaded file "{fileName}" and removed local copy\n')

        else:
            time.sleep(DETECT_DELAY)

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
