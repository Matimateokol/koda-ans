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

distr_data_set = [
    "geometr_05.pgm", "geometr_09.pgm", "geometr_099.pgm", "laplace_10.pgm", "laplace_20.pgm", "laplace_30.pgm",
    "normal_10.pgm", "normal_30.pgm", "normal_50.pgm", "uniform.pgm"
]

image_dir_path = "data/obrazy_testowe/"

image_data_set = [
    "barbara.pgm", "boat.pgm", "chronometer.pgm", "lena.pgm", "mandril.pgm", "peppers.pgm"
]

def run_entropy_test(datafile_name, data_folder_path):
    data_path = data_folder_path + datafile_name
    img = Image.open(data_path).convert("L")  # L = grayscale
    data = np.array(img)

    print("Data shape: ", data.shape)

    # Make a histogram
    # flattening to 1D
    data = data.flatten()
    hist = np.bincount(data, minlength=256)

    # Calculate entropy
    hist = hist[hist > 0]          # removing zeros
    probs = hist / hist.sum()
    H = -np.sum(probs * np.log2(probs))
    
    print(f"Entropia obrazu {datafile_name} :", H, "bit/piksel. [From Histogram]")
    print(f"Entropia obrazu {datafile_name} :", shannon_entropy(data, 256), "bit/piksel. [From Shannon Entropy]")


for distr_data_name in distr_data_set:
    run_entropy_test(distr_data_name, distr_dir_path)

for image_data_name in image_data_set:
    run_entropy_test(image_data_name, image_dir_path)