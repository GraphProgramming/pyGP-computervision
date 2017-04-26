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

def init(node, global_state):
    def tick(value):
        return {"calib": PinholeCamera(node["args"]["width"], node["args"]["height"], node["args"]["fx"], node["args"]["fy"], node["args"]["cx"], node["args"]["cy"],
                                       node["args"]["k1"], node["args"]["k2"], node["args"]["p1"], node["args"]["p2"], node["args"]["k3"], node["args"]["calibFile"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "Camera Calibration"
    node["outputs"]["calib"] = "Camera"
    node["args"]["width"] = 200
    node["args"]["height"] = 200
    node["args"]["fx"] = 718.856
    node["args"]["fy"] = 718.856
    node["args"]["cx"] = 607.1928
    node["args"]["cy"] = 128.2157
    node["args"]["k1"] = 0
    node["args"]["k2"] = 0
    node["args"]["p1"] = 0
    node["args"]["p2"] = 0
    node["args"]["k3"] = 0
    node["args"]["calibFile"] = "cam_calib.npz"
    node["desc"] = "Publishes a camera calibration."
