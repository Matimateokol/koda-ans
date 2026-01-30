import os
from pathlib import Path

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