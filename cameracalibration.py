from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

class PinholeCamera(object):
	def __init__(self, width, height, fx, fy, cx, cy, k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0, calibFile=None):
		self.width = width
		self.height = height
		self.fx = fx
		self.fy = fy
		self.cx = cx
		self.cy = cy
		self.distortion = (abs(k1) > 0.0000001)
		self.d = [k1, k2, p1, p2, k3]
		self.mtx = None
		self.dist = None
		self.rvecs = None
		self.tvecs = None

		if calibFile is not None:
			pass

@register(NODES,
    name="Camera Calibration",
    inputs=dict(),
    outputs=dict(calib="Camera"))
def init(node, global_state, width=200, height=200, fx=717.856, fy=718.856, cx=607.1928, cy=128.2157, k1=0, k2=0, k3=0, p1=0, p2=0, calibFile="cam_calib.npz") -> Callable:
    """
    Publishes a camera calibration.
    """
    def tick():
        return {"calib": PinholeCamera(width, height, fx, fy, cx, cy, k1, k2, p1, p2, k3, calibFile)}
    return tick
