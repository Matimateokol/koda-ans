import numpy as np

def shannon_entropy(data, alphabet_size=None):
    data = np.asarray(data)

    if alphabet_size is None:
        values, counts = np.unique(data, return_counts=True)
    else:
        counts = np.bincount(data, minlength=alphabet_size)
        counts = counts[counts > 0]

    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log2(probs))

    return entropy