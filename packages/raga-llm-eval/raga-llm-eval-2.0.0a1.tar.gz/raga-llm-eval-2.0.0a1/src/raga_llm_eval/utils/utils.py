"""
Helper functions
"""

import json
import uuid

import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy data types"""

    def default(self, obj):
        try:
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return super(NumpyEncoder, self).default(obj)
        except TypeError:
            print(f"Type not handled: {type(obj)}")
            raise


def generate_unique_name():
    """
    Generate a unique name for the test.

    Returns:
        str: A unique name for the test.
    """
    return str(uuid.uuid4())
