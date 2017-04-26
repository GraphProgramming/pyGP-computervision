def init(node, global_state):
    def tick(value):
        return {}

    node["tick"] = tick

def spec(node):
    node["name"] = "Depth Estimation"
    node["inputs"]["img1"] = "Image"
    node["inputs"]["img2"] = "Image"
    node["inputs"]["pose"] = "Pose"
    node["outputs"]["depth"] = "Image"
    node["desc"] = "Calculate a depth image given two images and their relative pose to each other."
