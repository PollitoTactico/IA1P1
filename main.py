# main.py

import os
import cv2
from pose_detector import PoseDetector
from feature_extractor import FeatureExtractor
from classifier import GolpeClassifier

# Buscar el último video subido
def obtener_ultimo_video(carpeta):
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".mp4")]
    if not archivos:
        print("❌ No se encontró ningún video en la carpeta 'subidos/'.")
        return None
    archivos.sort(key=lambda x: os.path.getmtime(os.path.join(carpeta, x)), reverse=True)
    return os.path.join(carpeta, archivos[0])

# Ruta al último video subido
video_path = obtener_ultimo_video("subidos")
if video_path is None:
    exit()

print(f"📹 Abriendo video: {video_path}")

# Inicializar componentes
detector = PoseDetector()
extractor = FeatureExtractor()
clasificador = GolpeClassifier()
clasificador.cargar_modelo("datos/modelo.pkl")

video = cv2.VideoCapture(video_path)
ventana = "Detección de Golpes (Vista manual)"

while True:
    ret, frame = video.read()
    if not ret:
        break

    landmarks = detector.detectar_pose(frame)
    if landmarks:
        vector = extractor.extraer_vector(landmarks)
        prediccion = clasificador.predecir(vector)
        cv2.putText(frame, f"Golpe: {prediccion}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(ventana, frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        print("Cerrado por el usuario.")
        break

video.release()
cv2.destroyAllWindows(ventana)  #cerrar solo esa ventana
