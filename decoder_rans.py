import struct
import sys
from model.cacl_distributor import rANSData, INTERVAL_SIZE, RENORM_LOWER, N_BITS

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