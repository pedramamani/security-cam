CAPTURE_SOURCE = 0


# Windows settings: 640x480@10/15/30, 1280x720@10/15/30, 1920x1080@10/15/30
# Raspbian settings: 1920x1088@30, 1280x720@60, 480p@60/90

class SETTING:
    resolution = (640, 480)
    frameRate = 60

class OS:
    windows = 'Windows'
    raspbian = 'Linux'