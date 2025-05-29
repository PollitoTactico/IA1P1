import numpy as np

class FeatureExtractor:
    def extraer_vector(self, landmarks):
        # Flatten the (x, y) list into a single vector
        return np.array([coord for point in landmarks for coord in point])