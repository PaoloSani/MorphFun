import cv2
import mediapipe as mp
import numpy as np
from pose_estimation.model import create_model
from utils import CONFIG_PATH, load_config

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR CONVERSION RGB 2 BGR
    return image, results


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh])


def init_model(model_path, sequence_length, actions):
    model = create_model(sequence_length, actions)
    model.load_weights(model_path)

    return model

def quit_estimation(cap):
    cap.release()
    cv2.destroyAllWindows()


def estimate_pose(model_path):
    config = load_config(CONFIG_PATH)

    actions = np.array(config['pose_estimation']['actions'])
    sequence_length = config['pose_estimation']['sequence_length']
    # 1. New detection variables
    sequence = []
    sentence = []
    predictions = []
    threshold = 0.6

    model = init_model(model_path, sequence_length, actions)

    cap = cv2.VideoCapture(0);
    # Set mediapipe model 
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():

            # Read feed
            ret, frame = cap.read()

            # Make detections
            image, results = mediapipe_detection(frame, holistic)
                        
            # 2. Prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-sequence_length:]
            
            if len(sequence) == sequence_length:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                prediction_value = res[np.argmax(res)]
                predicted_action = actions[np.argmax(res)]

                if prediction_value > threshold:
                    print(predicted_action)

                    if len(predictions) > 0: 
                            if predicted_action != predictions[-1]:
                                    predictions.append(predicted_action)
                            else:
                                predictions.append(predicted_action)
                
        
            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord('q'):
                quit_estimation(cap)
                break
        