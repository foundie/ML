import dlib
import cv2
import numpy as np

# Load the pre-trained facial landmark predictor
predictor_path = 'shape_predictor_68_face_landmarks.dat'  # You need to download this file
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Load the image
image_path = 'test_image.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = detector(gray)

if len(faces) > 0:
    # Assume there's only one face in the image
    face = faces[0]
    
    # Predict facial landmarks
    landmarks = predictor(gray, face)
    
    # Extract cheek landmarks (usually landmark points 1, 15, 4, and 12 in dlib)
    cheek_landmarks = np.array([[landmarks.part(1).x, landmarks.part(1).y],  # Left cheek
                                 [landmarks.part(15).x, landmarks.part(15).y],  # Right cheek
                                 [landmarks.part(4).x, landmarks.part(4).y],  # Left cheek
                                 [landmarks.part(12).x, landmarks.part(12).y]])  # Right cheek
    
    # Save the cheek landmarks to a file
    np.savetxt('cheek_landmarks.txt', cheek_landmarks, fmt='%d')
    
    print("Cheek landmarks saved to 'cheek_landmarks.txt'.")
else:
    print("No faces detected in the image.")
