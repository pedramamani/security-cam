import cv2
import platform



def main():
    print(platform.system())
    
    source = 0
    capture = cv2.VideoCapture(source)
    assert capture.isOpened(), f'failed to open capture {source}'

    while capture.isOpened():
        success, frame = capture.read()
        cv2.imshow('Live', frame)
        
        if cv2.waitKey(25) != -1:
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
