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

if __name__ == "__main__":
    # 
    ransdata = rANSData([0, 2, 3], [2, 1, 1], 2, 3)
    data = b'\x01\x00'
    rans_encode(data,ransdata)
    directory = Path.joinpath(Path.cwd(), "rozklady_testowe")
    # if directory.is_dir():
    #     with open(path, "rb") as f:
    #         while chunk := f.read(4096):
    #             a = rans_encode(chunk, calculate_distributor_list(directory))
    #             print(a)
    # else:
    #     print("no dir")