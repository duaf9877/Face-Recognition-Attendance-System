# src/train_model.py

print("✅ Python script is running")

from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import numpy as np
import os
import cv2
import pickle

# --- START of FIX ---
# Make the script location-aware to build correct paths
script_dir = os.path.dirname(os.path.abspath(__file__)) # Gets the directory of the script (e.g., /path/to/project/src)
project_root = os.path.dirname(script_dir) # Goes up one level to the project root

# Build robust paths to the dataset and model folders
dataset_dir = os.path.join(project_root, "dataset")
model_dir = os.path.join(project_root, "models")
# --- END of FIX ---

embedder = FaceNet()
X, y = [], []

print(f"[INFO] Looking for faces in: {dataset_dir}")
# Check if dataset directory exists
if not os.path.exists(dataset_dir) or not os.listdir(dataset_dir):
    print(f"[ERROR] Dataset directory is empty or does not exist at '{dataset_dir}'.")
    print("Please run capture_faces.py first to add images.")
    exit()

print("[INFO] Extracting faces and generating embeddings...")
for person in os.listdir(dataset_dir):
    person_dir = os.path.join(dataset_dir, person)
    if not os.path.isdir(person_dir):
        continue

    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        img = cv2.imread(img_path)
        if img is None:
            print(f"[WARN] Could not read image: {img_name}")
            continue

        try:
            embedding = embedder.embeddings([img])[0]
            X.append(embedding)
            y.append(person)
        except Exception as e:
            print(f"[WARN] Skipping {img_name} due to an error: {e}")

# Check if any faces were found
if not X:
    print("[ERROR] No faces were found in the dataset to train on. Exiting.")
    exit()

X = np.array(X)
y = np.array(y)

print("[INFO] Encoding labels and training model...")
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

model = SVC(kernel='linear', probability=True)
model.fit(X, y_encoded)

# Save model and label encoder
os.makedirs(model_dir, exist_ok=True) # Ensure the model directory exists

model_path = os.path.join(model_dir, "faces_recognition.pkl")
encoder_path = os.path.join(model_dir, "label_encoder.pkl")

pickle.dump(model, open(model_path, "wb"))
pickle.dump(encoder, open(encoder_path, "wb"))

print(f"[SUCCESS] Model trained and saved in '{model_dir}'")