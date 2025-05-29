import os
import cv2
import pandas as pd
from pose_detector import PoseDetector
from feature_extractor import FeatureExtractor
from classifier import GolpeClassifier

# Carpeta de videos y salida
VIDEO_FOLDER = "videos"
OUTPUT_FOLDER = "datos"
CSV_PATH = os.path.join(OUTPUT_FOLDER, "dataset.csv")
MODEL_PATH = os.path.join(OUTPUT_FOLDER, "modelo.pkl")

# Etiquetas según nombre de archivo
ETIQUETAS = {
    "bump": "mancheta",
    "set": "voleo",
    "remate": "remate"
}

# Inicializar clases
detector = PoseDetector()
extractor = FeatureExtractor()
X = []
y = []

# Procesar cada video
for nombre_archivo in os.listdir(VIDEO_FOLDER):
    ruta = os.path.join(VIDEO_FOLDER, nombre_archivo)
    etiqueta = None
    for clave in ETIQUETAS:
        if clave in nombre_archivo.lower():
            etiqueta = ETIQUETAS[clave]
            break
    if etiqueta is None:
        print(f"❌ Ignorado: {nombre_archivo}")
        continue

    print(f"📹 Procesando {nombre_archivo} como '{etiqueta}'")
    video = cv2.VideoCapture(ruta)
    frame_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Procesar solo 1 de cada 10 frames
        if frame_count % 10 == 0:
            landmarks = detector.detectar_pose(frame)
            if landmarks:
                vector = extractor.extraer_vector(landmarks)
                X.append(vector)
                y.append(etiqueta)
                print(f"✔ Frame {frame_count} procesado")

        frame_count += 1

    video.release()

# Guardar datos
df = pd.DataFrame(X)
df["etiqueta"] = y
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
df.to_csv(CSV_PATH, index=False)
print(f"✅ Dataset guardado en: {CSV_PATH}")

# Entrenar modelo
print("🧠 Entrenando modelo...")
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

le = LabelEncoder()
y_encoded = le.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

clasificador = GolpeClassifier()
clasificador.entrenar(X_train, y_train)

# Guardar modelo y etiquetas codificadas
import pickle
with open(MODEL_PATH, "wb") as f:
    pickle.dump((clasificador.modelo, le), f)

print(f"✅ Modelo guardado en: {MODEL_PATH}")
