import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from entropy.entropy import shannon_entropy
from histogram.histogram import histogram

distr_dir_path = "data/rozklady_testowe/"
distr_data_set = [
    "geometr_05.pgm", "geometr_09.pgm", "geometr_099.pgm", "laplace_10.pgm", "laplace_20.pgm", "laplace_30.pgm",
    "normal_10.pgm", "normal_30.pgm", "normal_50.pgm", "uniform.pgm"
]

image_dir_path = "data/obrazy_testowe/"
image_data_set = [
    "barbara.pgm", "boat.pgm", "chronometer.pgm", "lena.pgm", "mandril.pgm", "peppers.pgm"
]

#########################################################
# Wizualizacja histogramu
#########################################################

def plot_histogram(hist, title, hist_name):
    plt.figure()
    plt.bar(range(len(hist)), hist)
    plt.title(title)
    plt.xlabel("Symbol")
    plt.ylabel("Liczność")
    plt.savefig(hist_name)

img_paths = []
img_names = []
for distr in distr_data_set:
    img_names.append(distr)
    img_paths.append(distr_dir_path + distr)

for img in image_data_set:
    img_names.append(img)
    img_paths.append(image_dir_path + img)


for image_idx in range(len(img_names)):
    hist_img = histogram(img_paths[image_idx], alphabet_size=256)
    hist_name_path = "tests/outputs/" + img_names[image_idx][:-4] + ".png"
    org_name = img_names[image_idx]

    plot_histogram(hist_img, f"Histogram obrazu {org_name} (8-bit)", hist_name_path)

    image_idx += 1