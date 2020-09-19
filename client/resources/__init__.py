

import os

def get(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)

