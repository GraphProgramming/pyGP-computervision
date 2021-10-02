from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Depth Estimation",
    inputs=dict(img1="Image", img2="Image", pose="Pose"),
    outputs=dict(depth="Image"))
def init(node, global_state) -> Callable:
    """
    Calculate a depth image given two images and their relative pose to each other.
    """
    def tick(img1, img2, pose):
        return {"depth": None}
    return tick
