import numpy as np
from PIL import Image
from entropy.entropy import shannon_entropy
from histogram.histogram import histogram

image_dir_path = "data/obrazy_testowe/"
image_name = "lena.pgm"
image_path = image_dir_path + image_name

img = Image.open(image_path).convert("L")
img_data = np.array(img).flatten()

H_img = shannon_entropy(img_data, alphabet_size=256)
print("Entropia obrazu:", H_img)

hist_img = histogram(img_data, alphabet_size=256)

#########################################################
# Wizualizacja histogramu
#########################################################

import matplotlib.pyplot as plt

hist_name = image_name[:-4] + "_hist.png"

def plot_histogram(hist, title):
    plt.figure()
    plt.bar(range(len(hist)), hist)
    plt.title(title)
    plt.xlabel("Symbol")
    plt.ylabel("Liczność")
    # plt.show()
    plt.savefig(hist_name)

plot_histogram(hist_img, "Histogram obrazu (8-bit)")