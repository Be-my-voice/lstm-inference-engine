import base64
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
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

framecount = 0

while cap.isOpened():
    
    ret, frame = cap.read()

    if not ret:
        break

    framecount += 1

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        i = 0
        for landmarks in results.multi_hand_landmarks[0].landmark:
            arrx.append(landmarks.x)
            arry.append(landmarks.y)
            i += 1

        j = 0
        for landmarks in results.multi_hand_landmarks[0].landmark:
            arrx.append(landmarks.x)
            arry.append(landmarks.y)
            j += 1

        print(str(framecount) + " : " + str(i) +" | "+ str(j))

    #           mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    # cv2.imshow("HAND", frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

cap.release()
cv2.destroyAllWindows()

arrxnp = np.array(arrx)
arrynp = np.array(arry)

zerosx = (arrxnp == 0)

print(np.sum(zerosx))

print(arrxnp)
print(arrynp)

print(len(arrxnp))
print(len(arrynp))
print(framecount)