import dataclasses
from importlib.resources import path
import platform
import pathlib


@dataclasses.dataclass
class CameraConfig:
    isPiCamera: bool
    mode: int
    frameRate: int
    resolution: tuple[int, int]
    cropResolution: tuple[int, int] = None
    cropCenter: tuple[int, int] = None
    cropStart: tuple[int, int] = dataclasses.field(init=False)
    cropEnd: tuple[int, int] = dataclasses.field(init=False)

    def __post_init__(self):
        if self.cropResolution is None:
            self.cropResolution = self.resolution
        if self.cropCenter is None:
            self.cropCenter = (self.resolution[0] // 2, self.resolution[1] // 2)
        self.cropStart = (self.cropCenter[0] - self.cropResolution[0] // 2, self.cropCenter[1] - self.cropResolution[1] // 2)
        self.cropEnd = (self.cropCenter[0] + self.cropResolution[0] // 2, self.cropCenter[1] + self.cropResolution[1] // 2)


# Webcam: 640x480@10/15/30, 1280x720@10/15/30, 1920x1080@10/15/30
# Picam: 1920x1088@30, 1280x720@60, ... => https://picamera.readthedocs.io/en/release-1.13/fov.html

WEBCAM_CONFIG = CameraConfig(False, 0, 30, (640, 480))
PICAM_CONFIG = CameraConfig(True, 7, 10, (640, 480), (300, 300), (356, 254))
MAIN_CONFIG = WEBCAM_CONFIG if platform.system() == 'Windows' else PICAM_CONFIG

WARMUP_DELAY = 2  # seconds to wait for camera to warm up and adjust
DETECT_DELAY = 0.5  # seconds delay between detection instances
CAPTURE_COUNT = 2 * MAIN_CONFIG.frameRate  # frames saved in a capture instance
GNORM_THRESHOLD = 5

SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_FOLDER_ID = '1l3JiqF19aosyFD6ZShBCKGtWro6ItqJF'
ASSETS_DIR = pathlib.Path(__file__).parent.resolve() / 'assets'
TOKEN_FILE = ASSETS_DIR / 'token.json'
CREDS_FILE = ASSETS_DIR / 'creds.json'
