import cv2
from pose_detector import PoseDetector
from feature_extractor import FeatureExtractor
from classifier import GolpeClassifier

# Inicializar componentes
detector = PoseDetector()
extractor = FeatureExtractor()
clasificador = GolpeClassifier()
clasificador.cargar_modelo("datos/modelo.pkl")  # Usa el modelo entrenado

# Cambia este video por el que quieras probar
video = cv2.VideoCapture("videos/bump.mp4")

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Detectar pose
    landmarks = detector.detectar_pose(frame)
    if landmarks:
        # Extraer características
        vector = extractor.extraer_vector(landmarks)
        
        # Predecir tipo de golpe
        prediccion = clasificador.predecir(vector)
        print("Golpe detectado:", prediccion)

        # Mostrar predicción sobre el video
        cv2.putText(frame, f"Golpe: {prediccion}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Detección de Golpes", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Presiona ESC para salir
        break

video.release()
cv2.destroyAllWindows()
