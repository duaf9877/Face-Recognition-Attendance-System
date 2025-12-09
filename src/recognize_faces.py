# src/recognize_faces.py

import cv2
import numpy as np
import pickle
from keras_facenet import FaceNet
import os
from database_handler import create_table, mark_attendance

# --- FIX: Build absolute paths to model files ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
model_path = os.path.join(project_root, "models", "faces_recognition.pkl")
encoder_path = os.path.join(project_root, "models", "label_encoder.pkl")
# --- End of FIX ---

# ======================
# Load trained model
# ======================
print("[INFO] Loading model and encoder...")
try:
    model = pickle.load(open(model_path, "rb"))
    encoder = pickle.load(open(encoder_path, "rb"))
except FileNotFoundError:
    print("[ERROR] Model or encoder files not found.")
    print(f"Please make sure '{model_path}' and '{encoder_path}' exist.")
    print("Run train_model.py first.")
    exit()

embedder = FaceNet()

# ======================
# Initialize Database and Webcam
# ======================
print("[INFO] Initializing database...")
create_table()
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Cannot access webcam")
    exit()

print("[INFO] Starting face recognition. Press 'q' to quit.")
recognized_today = set() # To prevent marking the same person multiple times

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = embedder.extract(rgb, threshold=0.95)

    for face in faces:
        x1, y1, width, height = face["box"]
        x2, y2 = x1 + width, y1 + height
        face_img = frame[y1:y2, x1:x2]
        
        if face_img.size == 0:
            continue

        embedding = embedder.embeddings([face_img])[0]
        preds = model.predict_proba([embedding])[0]

        best_class = np.argmax(preds)
        confidence = preds[best_class]
        name = encoder.inverse_transform([best_class])[0] if confidence > 0.6 else "Unknown"

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{name} ({confidence*100:.1f}%)", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Mark attendance in the database
        if name != "Unknown" and name not in recognized_today:
            mark_attendance(name)
            recognized_today.add(name)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] Session ended. Attendance saved to the database.")