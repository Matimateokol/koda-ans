import struct
import os
import sys
from pathlib import Path
import argparse
from model.cacl_distributor import rANSData, calculate_model_from_data, RENORM_LOWER, N_BITS
from pgm_handler import read_pgm, format_size

def print_progress(current, total, prefix):
    percent = (current / total) * 100
    sys.stdout.write(f"\r{prefix}: [{percent:6.2f}%] ")
    sys.stdout.flush()

def rans_encode(data: bytes, model: rANSData) -> bytes:
    state = RENORM_LOWER
    stream = bytearray()
    limit_base = (RENORM_LOWER >> N_BITS) << 8
    
    total = len(data)
    for i, b in enumerate(reversed(data)):
        if i % 5000 == 0:
            print_progress(i, total, "[KODOWANIE]")

        freq = model.frequency[b]
        cdf = model.distributor[b]
        
        while state >= limit_base * freq:
            stream.append(state & 0xFF)
            state >>= 8
            
        state = ((state // freq) << N_BITS) + (state % freq) + cdf
        
    print_progress(total, total, "[KODOWANIE]")
    print(" - Gotowe!")
    
    res = bytearray(struct.pack("<I", state))
    res.extend(reversed(stream))
    return bytes(res)

def run_encoder(src_filename=None, dst_filename=None, base_dir_name=None):
    print("+++++ URUCHOMIONO APLIKACJĘ KODER +++++")
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_filename', dest='src_filename', type=str, help='A name of the file to be compressed.', default='')
    parser.add_argument('-d', '--dst_filename', dest='dst_filename', type=str, help='A name of the file after compression')
    parser.add_argument('-b', '--base_dir', dest='base_dir', type=str, help='Base dir relative path. Default is ./data/obrazy_testowe', default='./data/obrazy_testowe/')
    args = parser.parse_args()

    if args.dst_filename is None:
        args.dst_filename = f"{args.src_filename[:-4]}.rans"

    _src_filename = args.src_filename if (src_filename is None)  else src_filename
    _dst_filename = args.dst_filename if (dst_filename is None)  else dst_filename
    _base_dir_name = args.base_dir if (base_dir_name is None) else base_dir_name

    path = Path(_base_dir_name + _src_filename)

    if not path.exists():
        print("Plik nie istnieje!"); return

    header, pixels = read_pgm(path)
    orig_size = os.path.getsize(path)
    
    print(f"[*] Wczytano: {path.name} ({format_size(orig_size)})")
    model = calculate_model_from_data(pixels)
    
    encoded_body = rans_encode(pixels, model)
    
    out_path = Path(_base_dir_name + _dst_filename)
    with open(out_path, "wb") as f:
        f.write(b"RANS")
        for freq in model.frequency: f.write(struct.pack("<I", freq))
        f.write(struct.pack("<I", len(pixels)))
        f.write(struct.pack("<I", len(header)))
        f.write(header)
        f.write(encoded_body)
    
    comp_size = os.path.getsize(out_path)
    ratio = (comp_size / orig_size) * 100
    
    print("-" * 40)
    print(f"PLIK SKOMPRESOWANY: {out_path}")
    print(f"Oryginalny: {format_size(orig_size)}")
    print(f"Skompresowany: {format_size(comp_size)} (Stopień: {ratio:.2f}%)")
    print("-" * 40)
    

if __name__ == "__main__":
    run_encoder()