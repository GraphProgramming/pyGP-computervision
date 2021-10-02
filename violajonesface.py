import cv2
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Viola Jones Faces",
    inputs=dict(img="Image"),
    outputs=dict(img="Image"))
def init(node, global_state, width=320, height=240) -> Callable:
    """
    Face decetor using viola jones.
    """
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

    def tick(img):
        img = img.copy()
        img = cv2.resize(img, (width, height), 0, 0, cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #roi_gray = gray[y:y+h, x:x+w]
            #roi_color = img[y:y+h, x:x+w]
            #eyes = eye_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in eyes:
            #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        return {"img": img}
    return tick
