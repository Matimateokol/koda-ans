import os
from typing import List, Sequence
from dataclasses import dataclass
from pathlib import Path

N = 15
INTERVAL_SIZE = 2**N
NUMBER_OF_SYMBOLS = POSSIBLE_BYTES_VALUES = 256

@dataclass
class rANSData:
    distributor : List[int]
    frequency : List[int]
    interval_size : int
    renormalization_size : int

def byte_probabilities_from_directory(directory):
    counts = [0] * NUMBER_OF_SYMBOLS
    total_bytes = 0
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, "rb") as f:
                while chunk := f.read(4096):
                    for b in chunk:
                        counts[b] += 1
                    total_bytes += len(chunk)
    probabilities = [c / total_bytes for c in counts]
    return probabilities

def calculate_distributor_list(directory):
    probs = byte_probabilities_from_directory(directory)
    distributor = [0] * NUMBER_OF_SYMBOLS

    raw_freq = [p * INTERVAL_SIZE for p in probs]
    frequency = [max(1, round(x)) for x in raw_freq]
    freq_sum = sum(frequency)
    if INTERVAL_SIZE is not freq_sum:
        restore_interval_size_in_frequency(raw_freq, frequency, freq_sum)
        
    cur_sum = 0
    for i in range(NUMBER_OF_SYMBOLS - 1):
        cur_sum += frequency[i]
        distributor[i+1] = cur_sum
    distributor[-1] = INTERVAL_SIZE

    return rANSData(distributor, frequency, 15, 20)

def restore_interval_size_in_frequency(const_raw_freq: Sequence[float], frequency : List[int], const_freq_sum : int) -> None:
    errors = [(const_raw_freq[i] - frequency[i], i) for i in range(NUMBER_OF_SYMBOLS)]
    errors.sort()

    elements_to_add = abs(INTERVAL_SIZE - const_freq_sum)
    if (INTERVAL_SIZE - const_freq_sum > 0):
        errors.reverse()
        for _, i in errors:
            frequency[i] += 1
            elements_to_add -= 1
            if elements_to_add == 0:
                break
    else:
        for _, i in errors:
            if frequency[i] <= 1:
                continue
            frequency[i] -= 1
            elements_to_add -= 1
            if elements_to_add == 0:
                break

if __name__ == "__main__":
    directory = Path.joinpath(Path.cwd(), "rozklady_testowe")
    if directory.is_dir():
        a = calculate_distributor_list(directory)
        print(sum(a.frequency))
    else:
        print(f"error {directory} directory does not exist")
    