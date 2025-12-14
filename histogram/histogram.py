import numpy as np
from PIL import Image

def histogram(data_path, alphabet_size=None):
    """
    data: 1D array / bytes / list
    alphabet_size: eg. 256 for bytes (optional)
    """
    img = Image.open(data_path)
    data = np.asarray(img)
    data = data.ravel().astype(np.int64)

    if alphabet_size is None:
        values, counts = np.unique(data, return_counts=True)
        hist = dict(zip(values, counts))
    else:
        hist = np.bincount(data, minlength=alphabet_size)
    
    return hist