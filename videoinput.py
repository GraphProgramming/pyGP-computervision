import cv2
import time
import threading
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Video Input",
    inputs=dict(),
    outputs=dict(img="Image"))
def init(node, global_state, video=0, time_per_frame=0.2) -> Callable:
    """
    An opencv video capture
    """
    def image_producer():
        t = time_per_frame
        succ = True
        while succ:
            succ, img = node["capture"].read()
            global_state.publish(node, "img", img)
            time.sleep(t)

        global_state.shutdown_blockers -= 1
        
  
    def tick():
        global_state.shutdown_blockers += 1
        node["capture"] = cv2.VideoCapture(video)
        succ, img = node["capture"].read()
        t = threading.Thread(target=image_producer)
        t.setDaemon(True)
        t.start()
        return {"img": img}

    return tick
