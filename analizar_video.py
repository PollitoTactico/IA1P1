# analizar_video.py

import cv2
import csv
import os
from collections import Counter
from pose_detector import PoseDetector
from feature_extractor import FeatureExtractor
from classifier import GolpeClassifier

def analizar_video(ruta_video, output_dir="salidas"):
    os.makedirs(output_dir, exist_ok=True)

    detector = PoseDetector()
    extractor = FeatureExtractor()
    clasificador = GolpeClassifier()
    clasificador.cargar_modelo("datos/modelo.pkl")

    predicciones = []
    resultados_frame = []

    video = cv2.VideoCapture(ruta_video)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))

    nombre_base = os.path.splitext(os.path.basename(ruta_video))[0]
    ruta_video_salida = os.path.join(output_dir, f"{nombre_base}_procesado.mp4")
    ruta_csv_salida = os.path.join(output_dir, f"{nombre_base}_resultados.csv")

    out = cv2.VideoWriter(
        ruta_video_salida,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    frame_idx = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break

        pred = "Desconocido"
        landmarks = detector.detectar_pose(frame)
        if landmarks:
            vector = extractor.extraer_vector(landmarks)
            pred = clasificador.predecir(vector)
            predicciones.append(pred)

        # Escribir texto sobre el frame
        cv2.putText(frame, f"Golpe: {pred}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        out.write(frame)

        resultados_frame.append((frame_idx, pred))
        frame_idx += 1

    video.release()
    out.release()

    # Guardar resultados en CSV
    with open(ruta_csv_salida, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Frame", "Prediccion"])
        writer.writerows(resultados_frame)

    conteo = Counter(predicciones)
    return dict(conteo), ruta_video_salida, ruta_csv_salida
