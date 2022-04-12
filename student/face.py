import cv2
import numpy as np
from django.templatetags.static import static

def recognize(img):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    im = static('image.png')
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
    for(x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
        if(conf < 40):
            if(Id == 1):
                Id = "Manish"

        else:

            Id = "Unknown"
        # cv2.putText(cv2.cv.fromarray(im), str(Id), (x, y+h), font, 255)
        cv2.putText(im, str(Id), (x, y+h), font, 1, color=255)
        return Id
    # cv2.imshow('im', im)
    # cv2.destroyAllWindows()


# recognize()
