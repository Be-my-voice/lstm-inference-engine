import base64
import cv2
import mediapipe as mp
import numpy as np
import os
from moviepy.editor import VideoFileClip

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

directoryPath = "src_original"
outputDirectoryPath = "csv_files"

if not os.path.exists(outputDirectoryPath):
    os.makedirs(outputDirectoryPath)

subDirectories = os.listdir(directoryPath)

for item in subDirectories:
    content = os.listdir(directoryPath+"/"+item)
    if not os.path.exists(outputDirectoryPath+"/"+item):
        os.makedirs(outputDirectoryPath+"/"+item)
    for file in content:
        cap = cv2.VideoCapture(directoryPath+"/"+item+"/"+file)

        fnameWithoutExtension = os.path.splitext(file)[0]
        startOfFile = 1

        frameCount= 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break
            
            frameCount += 1

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(frame_rgb)
            # csv format -> frame1.lefthand.point1.x, frame1.lefthand.point1.y, frame1.lefthand.point2.x, frame1.lefthand.point2.y ......... frame1.lefthand.lastpoint.x, frame1.lefthand.lastpoint.y, frame1.righthand.point1.x, frame1.righthand.point1.y, ......
            with open(outputDirectoryPath+"/"+item+"/"+fnameWithoutExtension+".csv", mode='a', newline='') as file :
                if startOfFile == 0:
                    file.write("\n")
                
                startOfLine = 1

                if results.multi_hand_landmarks:
                    print("left starts")
                    for landmarks in results.multi_hand_landmarks[0].landmark:
                        print("left hand: ",landmarks.x,landmarks.y)
                        if startOfLine == 1:
                            file.write(str(landmarks.x)+","+str(landmarks.y))
                            startOfLine = 0
                        else:
                            file.write(","+str(landmarks.x)+","+str(landmarks.y))
                    
                    print("right starts")
                    print(len(results.multi_hand_landmarks[1].landmark))
                    for landmarks in results.multi_hand_landmarks[1].landmark:
                        print("right hand: ",landmarks.x,landmarks.y)
                        if startOfLine == 1:
                            file.write(str(landmarks.x)+","+str(landmarks.y))
                            startOfLine = 0
                        else:
                            file.write(","+str(landmarks.x)+","+str(landmarks.y))
                    
                #   for landmarks in results.multi_hand_landmarks:
                #       mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
                else:
                    print(0,0)
                    for i in range(42):
                        if startOfLine == 1:
                            file.write("0,0")
                            startOfLine = 0
                        else:
                            file.write(",0,0")
                    
            startOfFile = 0
            print(frameCount)
            # cv2.imshow(file, frame)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        
        
        cap.release()
        cv2.destroyAllWindows()
