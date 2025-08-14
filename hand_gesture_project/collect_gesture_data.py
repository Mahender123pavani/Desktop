import cv2
import mediapipe as mp
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

file = open("gesture_data.csv", mode='w', newline='')
writer = csv.writer(file)
print("Press 0 for Fist, 1 for Open Hand, 2 for Peace, 3 for Thumbs Up. Press ESC to exit.")

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
                key = cv2.waitKey(1)
                if key in [48, 49, 50, 51]:  # keys: 0-3
                    label = int(chr(key))
                    landmarks.append(label)
                    writer.writerow(landmarks)
                    print(f"Saved gesture for label {label}")

    cv2.imshow("Collecting Gesture Data", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
file.close()
cv2.destroyAllWindows()