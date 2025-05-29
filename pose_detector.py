import mediapipe as mp
import cv2

class PoseDetector:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
    
    def detectar_pose(self, frame): 
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)

        if results.pose_landmarks:
            # Convertir a lista simple (x, y)
            landmarks = []
            for lm in results.pose_landmarks.landmark:
                landmarks.append((lm.x, lm.y))
            return landmarks
        else:
            return None
