import struct
import sys
from pathlib import Path
import argparse
from model.cacl_distributor import rANSData, INTERVAL_SIZE, RENORM_LOWER, N_BITS
from pgm_handler import verify_files

def print_progress(current, total, prefix):
    percent = (current / total) * 100
    sys.stdout.write(f"\r{prefix}: [{percent:6.2f}%] ")
    sys.stdout.flush()

def rans_decode(data: bytes, model: rANSData, length: int) -> bytes:
    if not data: return b""
    
    state = struct.unpack("<I", data[:4])[0]
    ptr = 4
    out = bytearray()
    mask = INTERVAL_SIZE - 1
    
    for i in range(length):
        if i % 5000 == 0:
            print_progress(i, length, "[DEKODOWANIE]")

        slot = state & mask
        
        # Szybkie wyszukiwanie symbolu
        s = 0
        while model.distributor[s+1] <= slot:
            s += 1
            
        out.append(s)
        
        freq = model.frequency[s]
        cdf = model.distributor[s]
        state = freq * (state >> N_BITS) + (slot - cdf)
        
        while state < RENORM_LOWER and ptr < len(data):
            state = (state << 8) | data[ptr]
            ptr += 1
            
    print_progress(length, length, "[DEKODOWANIE]")
    print(" - Gotowe!")
    return bytes(out)


def run_decoder(src_filename=None, dst_filename=None, base_dir_name=None):
    print("+++++ URUCHOMIONO APLIKACJĘ DEKODER +++++")
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_filename', dest='src_filename', type=str, help='A name of the file to be decompressed.', default='')
    parser.add_argument('-d', '--dst_filename', dest='dst_filename', type=str, help='A name of the file after decompression')
    parser.add_argument('-b', '--base_dir', dest='base_dir', type=str, help='Base dir relative path. Default is ./data/obrazy_testowe', default='./data/obrazy_testowe/')
    args = parser.parse_args()

    if args.dst_filename is None:
        args.dst_filename = f"{args.src_filename[:-5]}_decoded.pgm"

    _src_filename = args.src_filename if (src_filename is None)  else src_filename
    _dst_filename = args.dst_filename if (dst_filename is None)  else dst_filename
    _base_dir_name = args.base_dir if (base_dir_name is None) else base_dir_name

    path = Path(_base_dir_name + _src_filename)

    if not path.exists():
        print("Plik nie istnieje!"); return

    with open(path, "rb") as f:
        freqs = [struct.unpack("<I", f.read(4))[0] for _ in range(256)]
        orig_size = struct.unpack("<I", f.read(4))[0]
        body = f.read()

    dist = [0] * 257
    for i in range(256): dist[i+1] = dist[i] + freqs[i]
    model = rANSData(dist, freqs)
    
    decoded = rans_decode(body, model, orig_size)
    
    out_path = Path(_base_dir_name + _dst_filename)
    with open(out_path, "wb") as f:
        f.write(decoded)
    
    print(f"[*] Zdekodowano do: {out_path}")
    
    # Próba weryfikacji, jeśli istnieje plik oryginalny
    original_candidate = path.with_suffix(".pgm")
    verify_files(original_candidate, out_path)


if __name__ == "__main__":
    run_decoder()