import cv2

def init(node, global_state):
    node["buffer_size"] = 1
    node["buffer_policy"] = "keep"
    
    def tick(value):
        img = value["img"]
        cam = value["cam"]
        
        if cam.mtx is None or cam.dist is None:
            return {"img": img}
        
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cam.mtx, cam.dist, (w,h), node["args"]["alpha"], (w,h))
        
        dst = cv2.undistort(img, cam.mtx, cam.dist, None, newcameramtx)
        
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + h]
        
        return {"img": dst}

    node["tick"] = tick

def spec(node):
    node["name"] = "Undistort"
    node["inputs"]["cam"] = "Camera"
    node["inputs"]["img"] = "Image"
    node["outputs"]["img"] = "Image"
    node["args"]["alpha"] = 1
    node["desc"] = "Does stuff"
