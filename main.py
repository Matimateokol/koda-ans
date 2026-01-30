import struct
import os
import sys
from pathlib import Path
from model.cacl_distributor import calculate_model_from_data, rANSData
from encoder_rans import rans_encode
from decoder_rans import rans_decode

BASE_DIR = "./data/obrazy_testowe/"

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB']:
        if size_bytes < 1024: return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} GB"

def read_pgm(path):
    with open(path, "rb") as f:
        header = f.readline() # P5
        while True:
            line = f.readline()
            header += line
            if not line.startswith(b"#"): break
        header += f.readline() # maxval
        data = f.read()
    return header, data

def verify_files(orig_path, dec_path):
    if not os.path.exists(orig_path) or not os.path.exists(dec_path):
        return
    orig = Path(orig_path).read_bytes()
    dec = Path(dec_path).read_bytes()
    if orig == dec:
        print("\n✅ WERYFIKACJA: Pliki są identyczne (bit-by-bit)!")
    else:
        print("\n❌ BŁĄD: Pliki różnią się od siebie!")

def main():
    print("\n" + "="*40)
    print(" rANS COMPRESSOR v1.0 ".center(40))
    print("="*40)
    
    mode = input("Wybierz aplikację (1=Koder, 2=Dekoder): ").strip()
    filename = input("Nazwa pliku: ").strip()
    path = Path(BASE_DIR + filename)

    if mode == "1":
        if not path.exists():
            print("Plik nie istnieje!"); return

        header, pixels = read_pgm(path)
        orig_size = os.path.getsize(path)
        
        print(f"[*] Wczytano: {path.name} ({format_size(orig_size)})")
        model = calculate_model_from_data(pixels)
        
        encoded_body = rans_encode(pixels, model)
        
        out_path = path.with_suffix(".rans")
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

    elif mode == "2":
        if not path.exists():
            print("Plik nie istnieje!"); return

        with open(path, "rb") as f:
            if f.read(4) != b"RANS":
                print("To nie jest plik RANS!"); return
            freqs = [struct.unpack("<I", f.read(4))[0] for _ in range(256)]
            orig_size = struct.unpack("<I", f.read(4))[0]
            hlen = struct.unpack("<I", f.read(4))[0]
            header = f.read(hlen)
            body = f.read()

        dist = [0] * 257
        for i in range(256): dist[i+1] = dist[i] + freqs[i]
        model = rANSData(dist, freqs)
        
        decoded = rans_decode(body, model, orig_size)
        
        out_path = path.with_suffix(".decoded.pgm")
        with open(out_path, "wb") as f:
            f.write(header)
            f.write(decoded)
        
        print(f"[*] Zdekodowano do: {out_path}")
        
        # Próba weryfikacji, jeśli istnieje plik oryginalny
        original_candidate = path.with_suffix(".pgm")
        verify_files(original_candidate, out_path)

if __name__ == "__main__":
    main()