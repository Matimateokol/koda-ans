from pathlib import Path

def run():

    original_filename = "data/obrazy_testowe/lena/lena.pgm"
    decompressed_filename = "data/obrazy_testowe/lena.decoded.pgm"

    original_data = Path(original_filename).read_bytes()
    transformed_data = Path(decompressed_filename).read_bytes()

    assert original_data == transformed_data
    

if __name__ == "__main__":
    run()