import numpy as np
from entropy.entropy import shannon_entropy

### Testy na własnych danych ###

# ROZKŁAD RÓWNOMIERNY #
N = 1_000_000
uniform_data = np.random.randint(0, 256, size=N)

H_uniform = shannon_entropy(uniform_data, alphabet_size=256)

print("Entropia (uniform):", H_uniform)

# ROZKŁAD NORMALNY (zdyskretyzowany) #
normal_data = np.random.normal(loc=128, scale=30, size=N)
normal_data = np.clip(normal_data, 0, 255).astype(np.uint8)

H_normal = shannon_entropy(normal_data, alphabet_size=256)
print("Entropia (normal):", H_normal)

# ROZKŁAD GEOMETRYCZNY #
p = 0.1
geo_data = np.random.geometric(p, size=N)
geo_data = np.clip(geo_data, 0, 255).astype(np.uint8)

H_geo = shannon_entropy(geo_data, alphabet_size=256)
print("Entropia (geometric):", H_geo)

# ROZKŁAD LAPLACE'A #
laplace_data = np.random.laplace(loc=128, scale=20, size=N)
laplace_data = np.clip(laplace_data, 0, 255).astype(np.uint8)

H_laplace = shannon_entropy(laplace_data, alphabet_size=256)
print("Entropia (laplace):", H_laplace)


### Testy na rozkładach testowych z zajęć ###

from PIL import Image
import numpy as np

distr_dir_path = "data/rozklady_testowe/"
distr_name = "geometr_05.pgm"
distr_path = distr_dir_path + distr_name

def load_pgm(path):
    img = Image.open(path).convert("L")  # L = grayscale
    data = np.array(img)
    return data

img = load_pgm(distr_path)
print(img.shape)

# Histogram #
def histogram_pgm(img):
    # flattening to 1D
    data = img.flatten()
    hist = np.bincount(data, minlength=256)
    return hist

hist = histogram_pgm(img)

# Entropia #

import numpy as np

def entropy_from_hist(hist):
    hist = hist[hist > 0]          # usuwamy zera
    probs = hist / hist.sum()
    return -np.sum(probs * np.log2(probs))

H = entropy_from_hist(hist)
print(f"Entropia obrazu {distr_name} :", H, "bit/piksel")