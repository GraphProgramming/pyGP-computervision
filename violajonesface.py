import cv2

def init(node, global_state):
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

    def tick(value):
        img = value["img"].copy()
        width = node["args"]["width"]
        height = node["args"]["height"]
        if width == 0:
            width = 320
        if height == 0:
            height = int(width * 3 / 4)
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
        return {"result": img}

    node["tick"] = tick

def spec(node):
    node["name"] = "Viola Jones Faces"
    node["inputs"]["img"] = "Image"
    node["outputs"]["result"] = "Image"
    node["args"]["width"] = 0
    node["args"]["height"] = 0
    node["desc"] = "Face detector using viola jones."
