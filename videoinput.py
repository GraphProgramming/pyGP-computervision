import cv2
import time
import threading

def init(node, global_state):
    def image_producer():
        t = node["args"]["time_per_frame"]
        succ = True
        while succ:
            succ, img = node["capture"].read()
            global_state.publish(node, "val", img)
            time.sleep(t)

        global_state.shutdown_blockers -= 1
        
  
    def tick(value):
        global_state.shutdown_blockers += 1
        node["capture"] = cv2.VideoCapture(node["args"]["video"])
        succ, img = node["capture"].read()
        t = threading.Thread(target=image_producer)
        t.setDaemon(True)
        t.start()
        return {"val": img}

    node["tick"] = tick

def spec(node):
    node["name"] = "Video Input"
    node["outputs"]["val"] = "Image"
    node["args"]["video"] = 0
    node["args"]["time_per_frame"] = 0.2
    node["desc"] = "An open cv video capture."
