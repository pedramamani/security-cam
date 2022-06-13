CAPTURE_SOURCE = 0

# Windows settings: 640x480@10/15/30, 1280x720@10/15/30, 1920x1080@10/15/30
# Raspbian settings: 1920x1088@30, 1280x720@60, more here https://picamera.readthedocs.io/en/release-1.13/fov.html

class SETTING:
    resolution = (1920, 1080)
    frameRate = 5
    duration = 10

class OS:
    windows = 'Windows'
    raspbian = 'Linux'

CAPTURE_DELAY = int(1000 / SETTING.frameRate * 0.3)  # multiplied by a correction factor
