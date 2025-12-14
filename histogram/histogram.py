import numpy as np

def histogram(data, alphabet_size=None):
    """
    data: 1D array / bytes / list
    alphabet_size: eg. 256 for bytes (optional)
    """
    data = np.asarray(data)

    if alphabet_size is None:
        values, counts = np.unique(data, return_counts=True)
        hist = dict(zip(values, counts))
    else:
        hist = np.bincount(data, minlength=alphabet_size)
    
    return hist