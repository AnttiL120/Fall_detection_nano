import cv2

class DrawObjects(object):
    
    def __init__(self, topology, keypoints):
        self.topology = topology
        self.keypoints = keypoints
        
    def __call__(self, image, object_counts, objects, normalized_peaks):
        topology = self.topology
        keypoints = self.keypoints
        height = image.shape[0]
        width = image.shape[1]
        color = (0, 255, 0)
        cv2.rectangle(image, (0, 0), (224, 224), color, 2)
        K = topology.shape[0]
        count = int(object_counts[0])
        K = topology.shape[0]
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
                    cv2.putText(image, keypoints[j], (x + 20, y), cv2.FONT_HERSHEY_PLAIN, 1, color, 1, cv2.LINE_AA)

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