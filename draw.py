#falling class values can be checked from human_pose.json
#Peak values are just initialized and are changed if spotted
import cv2

class DrawObjects(object):
    
    def __init__(self, topology):
        self.topology = topology
        self.nose_value = 0
        self.left_hip_value = 12
        self.right_hip_value = 13
        self.left_ankle_value = 15
        self.right_ankle_value = 16
        self.peak_nose_x = 10
        self.peak_left_ankle_x = 120
        self.peak_right_hip_x = 120
        self.peak_right_ankle_x = 224
        self.peak_left_ankle_x = 224

        
    def __call__(self, image, object_counts, objects, normalized_peaks):
        topology = self.topology
        height = image.shape[0]
        width = image.shape[1]
        K = topology.shape[0]
        count = int(object_counts[0])

        nose_value = self.nose_value
        left_ankle_value = self.left_ankle_value
        right_ankle_value = self.right_ankle_value
        left_hip_value = self.left_hip_value
        right_hip_value = self.right_hip_value
        peak_nose_x = self.peak_nose_x
        peak_right_ankle_x = self.peak_right_ankle_x
        peak_left_ankle_x = self.peak_left_ankle_x
        peak_left_hip_x = self.peak_left_ankle_x
        peak_right_hip_x = self.peak_right_ankle_x
        fall_limit_ankle = 170
        fall_limit_hip = 100
        ankle_check = fall_limit_ankle + peak_nose_x
        hip_check = fall_limit_hip + peak_nose_x

        for i in range(count):
            obj = objects[0][i]
            C = obj.shape[0]
            for j in range(C):
                k = int(obj[j])
                if k >= 0:
                    peak = normalized_peaks[0][j][k]
                    x = round(float(peak[1]) * width)
                    y = round(float(peak[0]) * height)

                    if j == nose_value:
                        peak_nose_x = y
                    elif j == left_ankle_value:
                        peak_left_ankle_x = y
                    elif j == right_ankle_value:
                        peak_right_ankle_x = y
                    elif j == left_hip_value:
                        peak_left_ankle_x = y
                    elif j == right_hip_value:
                        peak_right_ankle_x = y

                    if ankle_check > peak_right_ankle_x or ankle_check > peak_left_ankle_x or hip_check > peak_left_hip_x or hip_check > peak_right_hip_x:
                        standing = 'Human has fallen'
                        color = (0, 0, 255)
                    else:
                        standing = 'Human is standing'
                        color = (0, 255, 0)


                    cv2.circle(image, (x, y), 3, color, 2)
                    cv2.putText(image, standing,(20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                    cv2.putText(image, "nose:{}".format(peak_nose_x),(100, peak_nose_x), cv2.FONT_HERSHEY_SIMPLEX, 0.1, color, 1, cv2.LINE_AA)
                    cv2.putText(image, "l.ankle:{}".format(peak_left_ankle_x),(180, peak_left_ankle_x), cv2.FONT_HERSHEY_SIMPLEX, 0.1, color, 1, cv2.LINE_AA)
                    cv2.putText(image, "r.ankle:{}".format(peak_right_ankle_x),(0, peak_right_ankle_x), cv2.FONT_HERSHEY_SIMPLEX, 0.1, color, 1, cv2.LINE_AA)
                    cv2.putText(image, "r.hip:{}".format(peak_right_hip_x),(180, peak_right_hip_x), cv2.FONT_HERSHEY_SIMPLEX, 0.1, color, 1, cv2.LINE_AA)
                    cv2.putText(image, "l.hip:{}".format(peak_left_hip_x),(0, peak_left_hip_x), cv2.FONT_HERSHEY_SIMPLEX, 0.1, color, 1, cv2.LINE_AA)

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
                    cv2.line(image, (x0, y0), (x1, y1), color, 2)
        
        