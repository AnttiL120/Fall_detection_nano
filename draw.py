#falling class values can be checked from human_pose.json
import cv2

class DrawObjects(object):
    
    def __init__(self, topology):
        self.topology = topology
        self.nose_value = 0
        self.left_ankle_value = 14
        self.right_ankle_value = 15
        self.peak_nose = ([1], [1])
        self.peak_right_ankle = ([1], [1])
        self.peak_left_ankle = ([1], [1])

        
    def __call__(self, image, object_counts, objects, normalized_peaks):
        topology = self.topology
        height = image.shape[0]
        width = image.shape[1]
        K = topology.shape[0]
        count = int(object_counts[0])

        nose_value = self.nose_value
        left_ankle_value = self.left_ankle_value
        right_ankle_value = self.right_ankle_value
        peak_nose = self.peak_nose
        peak_right_ankle = self.peak_right_ankle
        peak_left_ankle = self.peak_left_ankle
        fall_limit = 150
        
        if (peak_nose[0] - fall_limit) < peak_right_ankle or peak_left_ankle:
            standing = 'Human is standing'
            color = (0, 0, 255)
        else:
            standing = 'Human might has fallen'
            color = (0, 255, 0)

        for i in range(count):
            obj = objects[0][i]
            C = obj.shape[0]
            for j in range(C):
                k = int(obj[j])
                if k >= 0:
                    peak = normalized_peaks[0][j][k]
                    x = round(float(peak[1]) * width)
                    y = round(float(peak[0]) * height)
                    cv2.circle(image, (x, y), 3, color, 2)
                    if j == nose_value:
                        peak_nose = ([x], [y])
                    elif j == left_ankle_value:
                        peak_left_ankle = ([x], [y])
                    elif j == right_ankle_value:
                        peak_right_ankle = ([x], [y])

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
        
        