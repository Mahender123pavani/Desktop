import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib
import time

# Load the dataset
data = pd.read_csv("gesture_data.csv")
X = data.iloc[:, :-1].values  # Features
y = data.iloc[:, -1].values   # Labels

# Train KNN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# Save the model (optional)
joblib.dump(knn, "knn_model.pkl")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Gesture labels
gesture_names = {
    0: "Fist",
    1: "Open Hand",
    2: "Peace",
    3: "Thumbs Up"
}

# Webcam capture
cap = cv2.VideoCapture(0)

print("Press ESC to exit...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y])

            if len(landmarks) == 42:
                prediction = knn.predict([landmarks])[0]
                gesture = gesture_names.get(prediction, "Unknown")

                # Show prediction on screen
                cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

                # Write result to a text file
                with open("gesture_output.txt", "w") as f:
                    f.write(gesture)

                # Add short delay
                time.sleep(0.15)

    cv2.imshow("Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()