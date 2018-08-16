import math
from sklearn import linear_model
import os
import os.path
import pickle
from PIL import Image, ImageDraw, ImageFont
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from tools import get_dominant_color, get_reverse_color
import shutil

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'}
ttfont = ImageFont.truetype("/Library/Fonts/SimHei.ttf", 12)

def train(train_dir, model_save_path=None, fit_intercept=True, normalize=False, verbose=False):
    """
    普通最小二乘线性回归 人脸识别.

    fit_intercept=True, normalize=False, copy_X=True, n_jobs=1

    :param train_dir: directory that contains a sub-directory for each known person, with its name.

     (View in source code to see train_dir example tree structure)

     Structure:
        <train_dir>/
        ├── <person1>/
        │   ├── <somename1>.jpeg
        │   ├── <somename2>.jpeg
        │   ├── ...
        ├── <person2>/
        │   ├── <somename1>.jpeg
        │   └── <somename2>.jpeg
        └── ...

    :param model_save_path: (optional) path to save model on disk
    :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
    :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
    :param verbose: verbosity of training
    :return: returns knn classifier that was trained on the given data.
    """
    X = []
    y = []

    allFolders = os.listdir(train_dir)
    # Loop through each person in the training set
    for num in range(len(allFolders)):
        class_dir = allFolders[num]
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        allImages = image_files_in_folder(os.path.join(train_dir, class_dir))
        # Loop through each training image for the current person
        for img_path in allImages:
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
                        face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(
                    image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

        print('AllFolder %s ,Current: (%.2f %%)' %
              (len(allFolders), num/len(allFolders)*100))


    # Create and train the Linear classifier
    linear_clf = linear_model.LinearRegression(fit_intercept,normalize)
    linear_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(linear_clf, f)

    return linear_clf


def predict(X_img_path, linear_clf=None, model_path=None, distance_threshold=0.6):
    """
    Recognizes faces in given image using a trained Linear classifier
 
    """
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if linear_clf is None and model_path is None:
        raise Exception(
            "Must supply knn classifier either thourgh linear_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if linear_clf is None:
        with open(model_path, 'rb') as f:
            linear_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(
        X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    # closest_distances = linear_clf.kneighbors(faces_encodings, n_neighbors=1)
    # are_matches = [closest_distances[0][i][0] <=
    #                distance_threshold for i in range(len(X_face_locations))]
 
    # Predict classes and remove classifications that aren't within the threshold
    result = []
    for pred, loc, rec in zip(linear_clf.predict(faces_encodings), X_face_locations):
        result.append((pred, loc) if rec else ("unknown", loc))
    return result



model_save_path = "downloads/train/trained_linear_model.clf"

if __name__ == "__main__":
    # STEP 1: Train the Linear classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.

    if not os.path.exists(model_save_path):
        print("Training Linear classifier...")
        classifier = train("downloads/train",
                           model_save_path=model_save_path)
        print("Training complete!")

