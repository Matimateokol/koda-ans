from encoder_rans import run_encoder
from decoder_rans import run_decoder

BASE_DIR = "./data/obrazy_testowe/"


def main():
    print("\n" + "="*40)
    print(" rANS COMPRESSOR v1.0 ".center(40))
    print("="*40)
    
    mode = input("Wybierz aplikację (1=Koder, 2=Dekoder): ").strip()
    src_filename = input("Nazwa pliku źródłowego: ").strip()
    dst_filename = input("Nazwa pliku docelowego: ").strip()
    base_dir_name = input("(Opcjonalnie) Nazwa folderu bazowego: ").strip()

    if base_dir_name is None or base_dir_name is "":
        base_dir_name = BASE_DIR

    if mode == "1":
        run_encoder(src_filename, dst_filename, base_dir_name)

    elif mode == "2":
        run_decoder(src_filename, dst_filename, base_dir_name)

if __name__ == "__main__":
    main()