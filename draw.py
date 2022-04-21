#falling class values can be checked from human_pose.json
#Peak values are just initialized and are changed if spotted
import cv2

class DrawObjects(object):
    
    def __init__(self, topology):
        self.topology = topology
        self.nose_value = 0
        self.left_hip_value = 12
        self.right_hip_value = 11
        self.left_ankle_value = 15
        self.right_ankle_value = 16
        self.peak_nose_y = 10
        self.peak_left_hip_y = 120
        self.peak_right_hip_y = 120
        self.peak_right_ankle_y = 224
        self.peak_left_ankle_y = 224
        self.check_stand = 0
        self.color = (0, 255, 0)
        self.standing = 'Human is standing'

        
    def __call__(self, image, object_counts, objects, normalized_peaks):
        topology = self.topology
        height = image.shape[0]
        width = image.shape[1]
        K = topology.shape[0]
        count = int(object_counts[0])

        fall_limit_ankle = 180
        fall_limit_hip = 120
        ankle_check = fall_limit_ankle + self.peak_nose_y
        hip_check = fall_limit_hip + self.peak_nose_y

        for i in range(count):
            obj = objects[0][i]
            C = obj.shape[0]
            for j in range(C):
                k = int(obj[j])
                if k >= 0:
                    peak = normalized_peaks[0][j][k]
                    x = round(float(peak[1]) * width)
                    y = round(float(peak[0]) * height)

                    if j == self.nose_value:
                        self.peak_nose_y = y
                    elif j == self.left_ankle_value:
                        self.peak_left_ankle_y = y
                    elif j == self.right_ankle_value:
                        self.peak_right_ankle_y = y
                    elif j == self.left_hip_value:
                        self.peak_left_ankle_y = y
                    elif j == self.right_hip_value:
                        self.peak_right_ankle_y = y

                    if self.check_stand > 100 or self.check_stand == 0:

                        if ankle_check > self.peak_right_ankle_y or ankle_check > self.peak_left_ankle_y or hip_check > self.peak_left_hip_y or hip_check > self.peak_right_hip_y:
                            self.standing = 'Human has fallen'
                            self.color = (0, 0, 255)
                        else:
                            self.standing = 'Human is standing'
                            self.color = (0, 255, 0)
                        self.check_stand = 0

                    self.check_stand += 1

                    cv2.circle(image, (x, y), 3, self.color, 2)
                    cv2.putText(image, self.standing,(20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1, cv2.LINE_AA)
                    cv2.line(image, (0, ankle_check), (224, ankle_check), self.color, 1)
                    cv2.line(image, (0, hip_check), (224, hip_check), self.color, 1)
                    cv2.line(image, (0, self.peak_left_ankle_y), (224, self.peak_left_ankle_y), self.color, 1)
                    cv2.line(image, (0, self.peak_right_ankle_y), (224, self.peak_right_ankle_y), self.color, 1)
                    cv2.line(image, (0, self.peak_left_hip_y), (224, self.peak_left_hip_y), self.color, 1)
                    cv2.line(image, (0, self.peak_right_hip_y), (224, self.peak_right_hip_y), self.color, 1)
                    #cv2.putText(image, "ankle_check:{}".format(ankle_check),(150, ankle_check), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1, cv2.LINE_AA)
                    #cv2.putText(image, "hip_check:{}".format(hip_check),(50, hip_check), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1, cv2.LINE_AA)
                    #cv2.putText(image, "l.ankle:{}".format(self.peak_left_ankle_y),(180, self.peak_left_ankle_y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, self.color, 1, cv2.LINE_AA)
                    #cv2.putText(image, "r.ankle:{}".format(self.peak_right_ankle_y),(0, self.peak_right_ankle_y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, self.color, 1, cv2.LINE_AA)
                    #cv2.putText(image, "r.hip:{}".format(self.peak_right_hip_y),(180, self.peak_right_hip_y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, self.color, 1, cv2.LINE_AA)
                    #cv2.putText(image, "l.hip:{}".format(self.peak_left_hip_y),(0, self.peak_left_hip_y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, self.color, 1, cv2.LINE_AA)

            #For loop for the lines
            for k in range(K):
                c_a = topology[k][2]
                c_b = topology[k][3]
                if obj[c_a] >= 0 and obj[c_b] >= 0:
                    peak0 = normalized_peaks[0][c_a][obj[c_a]]
                    peak1 = normalized_peaks[0][c_b][obj[c_b]]
                    x0 = round(float(peak0[1]) * width)
                    y0 = round(float(peak0[0]) * height)
                    x1 = round(float(peak1[1]) * width)
                    y1 = round(float(peak1[0]) * height)
                    cv2.line(image, (x0, y0), (x1, y1), self.color, 2)
        
        