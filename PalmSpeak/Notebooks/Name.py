import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


model = Sequential([
    LSTM(64, return_sequences=True, activation='relu', input_shape=(40, 126)),
    LSTM(128, return_sequences=True, activation='relu'),
    LSTM(64, return_sequences=False, activation='relu'),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(20, activation='softmax')  # Adjust the output layer according to your requirements
])

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

from tensorflow.keras.models import load_model


try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE_PATH = os.path.join(BASE_DIR, 'savmodel', 'Loadall.h5')
    model.load_weights(FILE_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading the model:", e)

colors = [(128,0,128), (128,0,128),(128,0,128),(128,0,128),(128,0,128),	(128,0,128),(128,0,128),(128,0,128),(128,0,128),(128,0,128),(128,0,128), (128,0,128), (128,0,128),(128,0,128),(128,0,128),(128,0,128),(128,0,128),(128,0,128),(128,0,128),(128,0,128)]
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    highest_prob_idx = np.argmax(res)
    highest_prob = res[highest_prob_idx]
    highest_prob_percentage = highest_prob * 100
    cv2.putText(output_frame, f'{actions[highest_prob_idx]}: {highest_prob_percentage:.2f}%', (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors[highest_prob_idx], 2, cv2.LINE_AA)
    return output_frame

import mediapipe as mp
import cv2
import numpy as np
import tensorflow as tf
from scipy import stats

# New detection variables
sequence = []
sentence = []
threshold = 0.9
predictions = []
actions = ['Aeroplane', 'Aid', 'Baby', 'best friend', 'Book', 'bowl', 'Briefly', 'Clock', 'computer screen', 'Doll', 'Door', 'Dot', 'finger', 'glass', 'hanger','House', 'jalebi', 'lamp', 'Not', 'table']
# Set mediapipe model 
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the BGR image to RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert back to BGR
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw right hand connections

def draw_styled_landmarks(image, results):
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

def extract_keypoints(results):
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([lh, rh])



cap = cv2.VideoCapture(0)



with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        
        # Draw landmarks
        draw_styled_landmarks(image, results)
        
        # 2. Prediction logic
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-40:]
        
        if len(sequence) == 40:
            res = model.predict(np.expand_dims(sequence, axis=0), verbose=0 )[0]
            predictions.append(np.argmax(res))
         #3. Viz logic
            if np.unique(predictions[-10:])[0] == np.argmax(res): 
                if res[np.argmax(res)] > threshold: 
                    if len(sentence) > 0: 
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])

            if len(sentence) > 5: 
                sentence = sentence[-5:]

            # Viz probabilities
            image = prob_viz(res, actions, image, colors)
            
        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (10,40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Show to screen
        cv2.imshow('OpenCV Feed', image)

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
