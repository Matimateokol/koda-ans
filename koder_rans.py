import math
import struct
from cacl_distributor import rANSData, calculate_distributor_list
from pathlib import Path

def rans_encode(data: bytes, model: rANSData) -> bytes:
    N = model.interval_size
    R = model.renormalization_size
    END_OF_INTERVAL = 1 << (R + 1)
    LAST_BITS = (1 << N) -1
    out = bytearray()
    state = 1 << R

    for b in reversed(data):
        freq = model.frequency[b]
        cdf = model.distributor[b]

        while state >= freq << R:
            out.extend(struct.pack('<B', state & ((1 << N) - 1)))
            state >>= N
        state = ((state // freq) << N) + (state % freq) + cdf
    out.extend(struct.pack('<I', state)) # <I - sends 4 bytes
    out.reverse()
    return bytes(out)


def rans_decode(data: bytes, model: rANSData):
    out = bytearray()
    N = model.interval_size
    R = model.renormalization_size

    # Last bytes were written as LE, but were later reversed, thus we can read them as BE
    state = int.from_bytes(data[0:4], 'big')
    mask = (1 << N) - 1
    START = 1 << R

    cursor = 4

    # Find s such that cdf(s) < x_i+1 & mask < cdf(s+1)
    def find_symbol(x_low):
        # assumes distributor is sorted CDF
        for s in range(len(model.distributor) - 1):
            if model.distributor[s] <= x_low < model.distributor[s + 1]:
                return s
        return len(model.distributor) - 1

    while cursor < len(data) or state != START:
        # --- decode symbol ---
        x_low = state & mask
        s = find_symbol(x_low)

        state = (
            model.frequency[s] * (state >> N)
            + x_low
            - model.distributor[s]
        )

        out.append(s)

        # --- renormalisation (slide 4) ---
        while state < START and cursor < len(data):
            state = (state << N) | data[cursor]
            cursor += 1

    return bytes(out)


if __name__ == "__main__":

    ransdata = rANSData([0, 2, 3], [2, 1, 1], 2, 4)
    data = b'\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x00\x01\x01\x01\x02\x00\x01\x01\x01\x02\x00\x01\x01\x01\x02\x00\x01\x02\x00\x01\x02\x00\x01\x01\x01\x02\x00\x01\x02\x00\x01\x02\x00\x01\x01\x01\x02\x00\x01\x02\x00\x01\x02\x00\x01\x01\x01\x02\x00\x01\x02\x00\x01\x02\x00\x00\x00\x00\x02\x00\x01\x02\x00\x02\x00\x01\x02\x00\x02\x00\x01\x02\x00'
    data *= 8
    # data = b'\x01\x00\x00\x00\x01\x01\x01\x00'

    encoded = rans_encode(data, ransdata)
    decoded = rans_decode(encoded, ransdata)
    print(data == decoded)

    directory = Path.joinpath(Path.cwd(), "rozklady_testowe")
    # if directory.is_dir():
    #     with open(path, "rb") as f:
    #         while chunk := f.read(4096):
    #             a = rans_encode(chunk, calculate_distributor_list(directory))
    #             print(a)
    # else:
    #     print("no dir")