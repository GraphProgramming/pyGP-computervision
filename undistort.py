import cv2
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Undistort",
    inputs=dict(cam="Camera", img="Image"),
    outputs=dict(img="Image"))
def init(node, global_state, alpha=1) -> Callable:
    """
    Does stuff.
    """
    node["buffer_size"] = 1
    node["buffer_policy"] = "keep"
    
    def tick(img, cam):
        
        if cam.mtx is None or cam.dist is None:
            return {"img": img}
        
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cam.mtx, cam.dist, (w,h), alpha, (w,h))
        
        dst = cv2.undistort(img, cam.mtx, cam.dist, None, newcameramtx)
        
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + h]
        
        return {"img": dst}
    return tick
