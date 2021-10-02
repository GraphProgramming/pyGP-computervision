import cv2
import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}


lk_params = dict(winSize  = (21, 21), 
		#maxLevel = 3,
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))


def featureTracking(image_ref, image_cur, px_ref):
    kp2, st, err = cv2.calcOpticalFlowPyrLK(image_ref, image_cur, px_ref, None, **lk_params)  #shape: [k,2] [k,1] [k,1]

    st = st.reshape(st.shape[0])
    kp1 = px_ref[st == 1]
    kp2 = kp2[st == 1]

    return kp1, kp2

class NodeData(object):
    def __init__(self):
        self.cam = None
        self.new_frame = None
        self.last_frame = None
        self.cur_R = None
        self.cur_t = None
        self.px_ref = None
        self.px_cur = None
        self.kMinNumFeature = 1500
        self.detector = cv2.FastFeatureDetector_create(threshold=25, nonmaxSuppression=True)


@register(NODES,
    name="Visual Odometry",
    inputs=dict(img="Image", cam="Camera"),
    outputs=dict(odom="Pose"))
def init(node, global_state) -> Callable:
    """
    Calculates the visual odometry. Output is a global pose.
    """
    node["buffer_size"] = 1
    node["buffer_policy"] = "keep"
    
    node["data"] = NodeData()
    
    def tick(img, cam):
        data = node["data"]
        data.new_frame = img
        data.cam = cam
        focal = data.cam.fx
        pp = (data.cam.cx, data.cam.cy)
        
        if data.px_ref is None:
          data.px_ref = data.detector.detect(data.new_frame)
          data.px_ref = np.array([x.pt for x in data.px_ref], dtype=np.float32)
        else:
          data.px_ref, data.px_cur = featureTracking(data.last_frame, data.new_frame, data.px_ref)
          E, mask = cv2.findEssentialMat(data.px_cur, data.px_ref, focal=focal, pp=pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
          _, R, t, mask = cv2.recoverPose(E, data.px_cur, data.px_ref, focal=focal, pp=pp)

          if data.cur_t is None or data.cur_R is None:
            data.cur_t = t
            data.cur_R = R
          else:
            data.cur_t = data.cur_t + data.cur_R.dot(t)
            data.cur_R = R.dot(data.cur_R)

          if data.px_ref.shape[0] < data.kMinNumFeature:
            data.px_cur = data.detector.detect(data.new_frame)
            data.px_cur = np.array([x.pt for x in data.px_cur], dtype=np.float32)
          data.px_ref = data.px_cur
        data.last_frame = data.new_frame
        return {"odom": (data.cur_R, data.cur_t)}
    return tick
