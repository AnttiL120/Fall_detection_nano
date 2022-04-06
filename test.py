import cv2
import numpy as np

class pos(object):
    
    def __init__(self, topology):
        self.topology = topology
        self.peaks = np.array([[],[]])
        self.lines = np.array([[],[],[],[]])

    def save(self, image, object_counts, objects, normalized_peaks):
        topology = self.topology
        peaks = self.peaks
        lines = self.lines
        height = image.shape[0]
        width = image.shape[1]
        K = topology.shape[0]
        count = int(object_counts[0])
        
        for i in range(count):
            obj = objects[0][i]
            C = obj.shape[0]
            for j in range(C):
                k = int(obj[j])
                if k >= 0:
                    peak = normalized_peaks[0][j][k]
                    x = round(float(peak[1]) * width)
                    y = round(float(peak[0]) * height)
                    peaks = np.append(peaks[0], (x), axis=0)
                    peaks = np.append(peaks[1], (y), axis=0)


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
                    lines = np.append(lines[0], (x0), axis=0)
                    lines = np.append(lines[1], (y0), axis=0)
                    lines = np.append(lines[2], (x1), axis=0)
                    lines = np.append(lines[3], (y1), axis=0)

    def load():
        return
    
    def empty_arrays():