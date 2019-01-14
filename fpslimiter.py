import time

def init(node, global_state):
    node["last_transmission"] = 0
    def tick(value):
        result = {"img": value["img"]}
        now = time.time()
        if now - node["last_transmission"] < 1.0 / node["args"]["max_fps"]:
            return None
        
        node["last_transmission"] = now
        return result

    node["tick"] = tick

def spec(node):
    node["name"] = "FPS Limiter"
    node["inputs"]["img"] = "Image"
    node["outputs"]["img"] = "Image"
    node["args"]["max_fps"] = 4
    node["desc"] = "Limit the fps"
