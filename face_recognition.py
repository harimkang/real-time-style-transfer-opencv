import cv2


class FaceRecognition:
    def __init__(self):
        self.face_classifier = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')

    def predict(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return None

        return faces
