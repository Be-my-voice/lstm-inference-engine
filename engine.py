import base64
import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

arrx = []
arry = []

file = open("break_7.txt", "rb") 
text = file.read()
file.close()

fh = open("tempFiles/video.avi", "wb")
fh.write(base64.b64decode(text))
fh.close()

# the temperary converted video generated from base64 file should be in the tempFiles folder named "video.avi"
cap = cv2.VideoCapture("tempFiles/video.avi")

while cap.isOpened():
    
    ret, frame = cap.read()

    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks[0].landmark:
            arrx.append(landmarks.x)
            arry.append(landmarks.y)

        for landmarks in results.multi_hand_landmarks[1].landmark:
            arrx.append(landmarks.x)
            arry.append(landmarks.y)

        continue

    #           mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    # cv2.imshow("HAND", frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    for i in range(42):
        arrx.append(0)
        arry.append(0)

    print(arrx)
    print(arry)

cap.release()
cv2.destroyAllWindows()

# x coordinates
arrxnp = np.array(arrx)
# y coordinates
arrynp = np.array(arry)

print(arrxnp)
print(arrynp)