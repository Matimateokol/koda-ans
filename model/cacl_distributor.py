from dataclasses import dataclass
from typing import List

# Stałe rANS
N_BITS = 12
INTERVAL_SIZE = 1 << N_BITS  # 4096
RENORM_LOWER = 1 << 16      # Próg renormalizacji (2^16)

@dataclass
class rANSData:
    distributor: List[int]
    frequency: List[int]

def calculate_model_from_data(data: bytes) -> rANSData:
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    
    total = len(data) if len(data) > 0 else 1
    freqs = [0] * 256
    
    # Skalowanie do INTERVAL_SIZE (4096)
    for i in range(256):
        if counts[i] > 0:
            f = (counts[i] * INTERVAL_SIZE) // total
            freqs[i] = max(1, f)
            
    # Korekta sumy częstotliwości
    diff = INTERVAL_SIZE - sum(freqs)
    indices = sorted(range(256), key=lambda i: counts[i], reverse=True)
    for i in indices:
        if diff == 0: break
        if diff > 0:
            freqs[i] += 1
            diff -= 1
        elif diff < 0 and freqs[i] > 1:
            freqs[i] -= 1
            diff += 1

    # Budowa CDF
    dist = [0] * 257
    for i in range(256):
        dist[i+1] = dist[i] + freqs[i]
        
    return rANSData(dist, freqs)