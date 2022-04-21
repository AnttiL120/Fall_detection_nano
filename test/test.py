import numpy as np

class pos(object):
    
    def __init__(self, topology):
        self.topology = topology
        self.peaks = np.zeros((2,18,1))
        self.lines = np.zeros((4,18,1))
        self.height = 224
        self.width = 224

    def save(self, object_counts, objects, normalized_peaks):
        topology = self.topology
        peaks = self.peaks
        lines = self.lines
        height = self.height
        width = self.width
        K = topology.shape[0]
        count = int(object_counts[0])
        
        for i in range(count):
            obj = objects[0][i]
            C = obj.shape[0]

            a = np.zeros((2, C, 1), dtype=float)
            for j in range(C):
                k = int(obj[j])
                if k >= 0:
                    peak = normalized_peaks[0][j][k]
                    x = round(float(peak[1]) * width)
                    y = round(float(peak[0]) * height)
                    np.put(a, [j], [x])
                    np.put(a, [j + count], [y])
                else:
                    np.put(a, [j], [0])
                    np.put(a, [j + count], [0])

            peaks = np.append(peaks, a, axis=2)


                    
            b = np.zeros((count, K, 1))
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
                    np.put(b, [k], [x0])
                    np.put(b, [k + K], [y0])
            lines = np.append(lines, b, axis=2)


    def calc_data():
        return