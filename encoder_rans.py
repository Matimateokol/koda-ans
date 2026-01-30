import struct
import sys
from model.cacl_distributor import rANSData, INTERVAL_SIZE, RENORM_LOWER, N_BITS

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