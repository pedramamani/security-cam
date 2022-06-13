CAPTURE_SOURCE = 0


# Windows settings: 640x480@10/15/30, 1280x720@10/15/30, 1920x1080@10/15/30
# Raspbian settings: 1920x1088@30, 720@60, 480p@60/90

class SETTING:
    resolution = (1280, 720)
    frameRate = 60

class OS:
    windows = 'Windows'
    raspbian = 'Linux'