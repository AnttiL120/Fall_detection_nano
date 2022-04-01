import cv2

WIDTH = 224
HEIGHT = 224

class capture_video(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, image):
        name = self.name

        size = (WIDTH, HEIGHT)
        result = cv2.VideoWriter(name,
                        cv2.VideoWriter_fourcc(*'XVID'),
                        10, size)
        result.write(image)