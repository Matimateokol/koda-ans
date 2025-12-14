from cacl_distributor import rANSData, calculate_distributor_list, calculateModelForData
from pathlib import Path


def rans_encode(data: bytes, model: rANSData) -> int:
    N = model.interval_size
    R = model.renormalization_size
    state = 1 << R

    for b in reversed(data):
        freq = model.frequency[b]
        state = ((state // freq) << N) + (state % freq) + model.distributor[b]

    return state


def rans_decode(state: int, model: rANSData):
    out = bytearray()

    N = model.interval_size
    R = model.renormalization_size
    mask = (2 ** N) - 1

    while state != (1 << R):
        # Find s such that cdf(s) < x_i+1 & mask < cdf(s+1)
        s = len(model.distributor) - 1
        for s_i in range(0, len(model.distributor) - 1):
            if model.distributor[s_i] <= (state & mask) < model.distributor[s_i + 1]:
                s = s_i

        out.append(s)
        state = model.frequency[s] * (state >> N) + (state & mask) - model.distributor[s]

    return bytes(out)


if __name__ == "__main__":
    ransdata = rANSData([0, 2, 3], [2, 1, 1], 8, 3)

    data = b'\x01\x00\x00\x00\x01\x02\x01\x01\x00'
    encoded = rans_encode(data, ransdata)
    decoded = rans_decode(encoded, ransdata)
    assert data == decoded
    print(encoded.bit_length())

    print("### TEST on image data ###")

    from PIL import Image
    import numpy as np

    data_path = "data/obrazy_testowe/boat.pgm"
    img = Image.open(data_path).convert("L")  # L = grayscale
    data = np.array(img).flatten()
    ransdata = calculateModelForData(data)

    #data = b'\x01\x00\x00\x00\x01\x02\x01\x01\x00'
    encoded = rans_encode(data, ransdata)
    decoded = rans_decode(encoded, ransdata)
    assert data == decoded
    print(encoded.bit_length())
