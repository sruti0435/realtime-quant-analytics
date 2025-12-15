import numpy as np

def compute_spread(x, y, beta):
    spread = y - beta * x
    z = (spread - spread.mean()) / spread.std()
    return spread, z
