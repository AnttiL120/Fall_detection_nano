import cv2

video = cv2.VideoCapture(0)

if (video.isOpened() == False):
    print("Error reading video file")

frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)

result = cv2.VideoWriter('test.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

while (True):
    ret, frame = video.read()

    if ret == True:

        result.write(frame)

        if cv2.waitKey(32) & 0xFF == ord('s'):
            break
    else:
        break

video.release()
result.release()

cv2.destroyAllWindows()
print("The video was successfully saved")