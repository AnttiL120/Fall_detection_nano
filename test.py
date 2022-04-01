import sys
import cv2

def read_cam():
    video = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !  appsink")
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)

    result = cv2.VideoWriter('test.avi',
                        cv2.VideoWriter_fourcc(*'MJPG'),
                        10, size)

    if video.isOpened():
        cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
        while True:
            ret_val, frame = video.read()
            result.write(frame)
    else:
        print ("camera open failed")

    video.release()
    result.release()
    cv2.destroyAllWindows()
    print("The video was successfully saved")


if __name__ == '__main__':
    read_cam()