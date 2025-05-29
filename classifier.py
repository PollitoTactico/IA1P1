import pickle

class GolpeClassifier:
    def __init__(self):
        self.modelo = None
        self.encoder = None

    def entrenar(self, X, y):
        from sklearn.svm import SVC
        self.modelo = SVC(kernel='linear')
        self.modelo.fit(X, y)

    def cargar_modelo(self, ruta):
        with open(ruta, "rb") as f:
            self.modelo, self.encoder = pickle.load(f)

    def predecir(self, vector):
        if self.modelo:
            pred_encoded = self.modelo.predict([vector])[0]
            return self.encoder.inverse_transform([pred_encoded])[0]
        else:
            return "Desconocido"
