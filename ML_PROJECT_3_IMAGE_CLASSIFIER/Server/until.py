import joblib
import json
import os
import numpy as np
import base64
import cv2
from wavelet import w2d

__class_number_to_name = []
__class_name_to_number = []
__model = None



def get_image_from_b64_image_string(b64_str):   
    encoded_data = b64_str.split(',')[1]
    decoded_data = base64.b64decode(encoded_data)
    nparr = np.frombuffer(decoded_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def classify_image(image_b64_data, file_path=None):
    imgs = get_cropped_img_with_2_eyes(file_path, image_b64_data)
    
    if not imgs:
        print("No valid images for classification.")
        return []

    result = []
    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))

        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3, 1), 
                                  scalled_img_har.reshape(32*32, 1)))
        len_img_array = 32*32*3 + 32*32

        final = combined_img.reshape(1, len_img_array).astype(float)
        
        # Reshape final and predict
        prediction = __model.predict(final)  # Ensure final is 2D
        result.append({
            'class' : class_number_to_name(prediction[0]),
            'class_probability' : np.round(__model.predict_proba(final)*100, 2).tolist()[0],
            'class_dict' :  __class_name_to_number
        })

    return result



def get_cropped_img_with_2_eyes(img_path, image_b64_data):
    face_cascade = cv2.CascadeClassifier("C:/Users/Kishor/ML_PROJECT_3_IMAGE_CLASSIFIER/Server/opencv/haarcascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("C:/Users/Kishor/ML_PROJECT_3_IMAGE_CLASSIFIER/Server/opencv/haarcascades/haarcascade_eye.xml")

    if img_path:
        img = cv2.imread(img_path)
    else:
        img = get_image_from_b64_image_string(image_b64_data)

    if img is None:
        print("Error: Image is None.")
        return []

    # print(f"Image shape before grayscale conversion: {img.shape}")

    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img  # Image is already grayscale

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        print("No faces detected.")
        return []

    cropped_faces = []
    for (x, y, w, h) in faces:
        if w < 20 or h < 20:
            print("Skipping small face region.")
            continue
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)

    return cropped_faces

def get_b64_test_image_for_sharapova():
    with open ("C:/Users/Kishor/ML_PROJECT_3_IMAGE_CLASSIFIER/Server/base64.txt") as f:
        return f.read()

def load_saved_artifacts():
    print("loading saved artifacts....Start")
    global __class_number_to_name
    global __class_name_to_number
    global __model

    with open("C:/Users/Kishor/ML_PROJECT_3_IMAGE_CLASSIFIER/Server/artifacts/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}

    if __model is None:
        with open("C:/Users/Kishor/ML_PROJECT_3_IMAGE_CLASSIFIER/Server/artifacts/saved_model.pkl", "rb") as f:
            __model = joblib.load(f)

    print("loading saved artifacts....Done")

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]


if __name__ == "__main__":
    load_saved_artifacts()
    # print(classify_image(get_b64_test_image_for_sharapova(), None))
    # print(classify_image(None, 'C:/Users/Kishor/ML_PROJECT_3_IMAGE_CLASSIFIER/Server/test_images/messi2.jpeg'))