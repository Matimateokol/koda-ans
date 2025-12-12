import struct
from cacl_distributor import rANSData, calculate_distributor_list
from pathlib import Path

def rans_encode(data: bytes, model: rANSData) -> bytes:
    N = model.interval_size
    R = model.renormalization_size
    END_OF_INTERVAL = 1 << (R + 1)
    out = bytearray()
    state = 1 << R

    for b in reversed(data):
        freq = model.frequency[b]
        cdf = model.distributor[b]
        
        state = ((state // freq) << N) + (state % freq) + cdf
        while state >= END_OF_INTERVAL:
            out.extend(struct.pack('<B', state & N)) # <B - sends 1 byte
            state >>= N

    out.extend(struct.pack('<I', state)) # <I - sends 4 bytes
    out.reverse()
    return bytes(out)


def rans_decode(data: bytes, model: rANSData):
    out = bytearray()
    N = model.interval_size
    R = model.renormalization_size

    # Last bytes were written as LE, but were later reversed, thus we can read them as BE
    state = int.from_bytes(data[0:4], 'big')
    mask = (2 ** N) - 1
    cursor = 4

    # Find s such that cdf(s) < x_i+1 & mask < cdf(s+1)
    def get_symbol():
        for s_i in range(0, len(model.distributor) - 1):
            if model.distributor[s_i] <= (state & mask) < model.distributor[s_i + 1]:
                return s_i
        else:
            return len(model.distributor) - 1

    END_OF_INTERVAL = 1 << (R + 1)

    while cursor < len(data):
        while state < END_OF_INTERVAL:
            state <<= N
            state |= data[cursor]
            cursor += 1
        s = get_symbol()
        out.append(s)
        state = model.frequency[s] * (state >> N) + (state & mask) - model.distributor[s]

    return bytes(out)


if __name__ == "__main__":

    ransdata = rANSData([0, 2, 3], [2, 1, 1], 2, 3)
    data = b'\x01\x00'

    encoded = rans_encode(data, ransdata)
    decoded = rans_decode(encoded, ransdata)
    assert data == decoded

    directory = Path.joinpath(Path.cwd(), "rozklady_testowe")
    # if directory.is_dir():
    #     with open(path, "rb") as f:
    #         while chunk := f.read(4096):
    #             a = rans_encode(chunk, calculate_distributor_list(directory))
    #             print(a)
    # else:
    #     print("no dir")