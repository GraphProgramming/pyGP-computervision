import time
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="FPS Limiter",
    inputs=dict(img="Image"),
    outputs=dict(img="Image"))
def init(node, global_state, max_fps=4) -> Callable:
    """
    Limit the fps.
    """
    node["last_transmission"] = 0
    def tick(img):
        result = {"img": img}
        now = time.time()
        if now - node["last_transmission"] < 1.0 / max_fps:
            return None
        
        node["last_transmission"] = now
        return result
    return tick
