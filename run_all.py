import os

from encoder_rans import run_encoder

print("-"*40)
print("Making histograms")
print("-"*40)
import tests.histogram_tests
print("-"*40)
print("\n")

print("-"*40)
print("Calculating input entropy")
print("-"*40)
import tests.entropy_tests
print("-"*40)
print("\n")

from encoder_rans import run_encoder
from decoder_rans import run_decoder

distr_data_set = ["rozklady_testowe/" + i for i in [
    "geometr_05.pgm", "geometr_09.pgm", "geometr_099.pgm", "laplace_10.pgm", "laplace_20.pgm", "laplace_30.pgm",
    "normal_10.pgm", "normal_30.pgm", "normal_50.pgm", "uniform.pgm"
]]
image_data_set = ["obrazy_testowe/" + i for i in [
    "barbara.pgm", "boat.pgm", "chronometer.pgm", "lena.pgm", "mandril.pgm", "peppers.pgm"
]]
data_set = distr_data_set + image_data_set

os.makedirs("run/compressed/rozklady_testowe", exist_ok=True)
os.makedirs("run/compressed/obrazy_testowe", exist_ok=True)
os.makedirs("run/decompressed/obrazy_testowe", exist_ok=True)
os.makedirs("run/decompressed/rozklady_testowe", exist_ok=True)

print("-"*40)
print("Compressing")
print("-"*40)

for f in data_set:
    run_encoder(src_filename=("data/"+f), dst_filename=("run/compressed/" + f[:-4]+".rans"), base_dir_name="./")

print("-"*40)
print("Uncompressing")
print("-"*40)

for f in data_set:
    run_decoder(src_filename=("run/compressed/"+f[:-4]+".rans"), dst_filename=("run/decompressed/" + f), base_dir_name="./")

print("-"*40)
print("Identity tests")
print("-"*40)

from pathlib import Path

for f in data_set:
    print(f"Checking {f}..")

    original_filename = "data/" + f
    decompressed_filename = "run/decompressed/" + f

    original_data = Path(original_filename).read_bytes()
    transformed_data = Path(decompressed_filename).read_bytes()

    assert original_data == transformed_data

print("OK!!!")



