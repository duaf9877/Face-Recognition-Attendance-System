import cv2
import os
from mtcnn import MTCNN

# -----------------------------
# Configuration
# -----------------------------
DATASET_PATH = "dataset"   # Folder where student images will be stored
PHOTOS_PER_PERSON = 50     # Number of photos to capture per student
CAMERA_ID = 0              # Default webcam

# -----------------------------
# Create dataset directory if not exists
# -----------------------------
if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)
    print(f"[INFO] Created dataset directory at: {DATASET_PATH}")

# -----------------------------
# Initialize face detector
# -----------------------------
detector = MTCNN()

# -----------------------------
# Ask for student's name
# -----------------------------
student_name = input("Enter student name: ").strip()
student_folder = os.path.join(DATASET_PATH, student_name)

# Create folder for this student
if not os.path.exists(student_folder):
    os.makedirs(student_folder)
    print(f"[INFO] Created folder for {student_name} at: {student_folder}")
else:
    print(f"[INFO] Folder for {student_name} already exists. New images will be added.")

# -----------------------------
# Start webcam
# -----------------------------
cap = cv2.VideoCapture(CAMERA_ID)
print("[INFO] Starting camera... Press 'q' to quit early.")

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to capture frame from camera.")
        break

    # Detect faces
    faces = detector.detect_faces(frame)
    for face in faces:
        x, y, width, height = face['box']
        x, y = abs(x), abs(y)
        cropped_face = frame[y:y + height, x:x + width]

        if cropped_face.size > 0:
            count += 1
            face_filename = os.path.join(student_folder, f"{student_name}_{count}.jpg")
            cv2.imwrite(face_filename, cropped_face)
            print(f"[INFO] Saved: {face_filename}")

            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.putText(frame, f"{count}/{PHOTOS_PER_PERSON}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Show frame
    cv2.imshow("Capturing Faces", frame)

    # Stop capturing if done or pressed 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Manual exit requested.")
        break
    elif count >= PHOTOS_PER_PERSON:
        print(f"[INFO] Collected {PHOTOS_PER_PERSON} images for {student_name}.")
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()
print("[INFO] Capture completed successfully!")