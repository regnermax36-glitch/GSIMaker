import os
import shutil
import subprocess
import zipfile
from cgsi import call, extract_partitions_from_payload, Sdat2img, gettype, imgextractor, IMG_DIR

class AdvancedExtractor:
    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def extract_and_decompose(self, rom_zip: str, label: str):
        target_dir = os.path.join(self.work_dir, label)
        extract_tmp = os.path.join(target_dir, "EXTRACT")
        img_tmp = os.path.join(target_dir, "IMG")
        decomp_tmp = os.path.join(target_dir, "DECOMPOSED")
        os.makedirs(extract_tmp, exist_ok=True)
        os.makedirs(img_tmp, exist_ok=True)
        os.makedirs(decomp_tmp, exist_ok=True)

        print(f"[{label}] Decompressing ZIP: {rom_zip}")
        with zipfile.ZipFile(rom_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_tmp)

        # Handle payload.bin
        payload = os.path.join(extract_tmp, "payload.bin")
        if os.path.exists(payload):
            print(f"[{label}] Extracting Payload.bin...")
            with open(payload, "rb") as f:
                extract_partitions_from_payload(f, ['system', 'product', 'system_ext', 'vendor'], extract_tmp, 4)

        # Process sparse/dat files
        for part in ['system', 'product', 'system_ext', 'vendor']:
            br_file = os.path.join(extract_tmp, f"{part}.new.dat.br")
            if os.path.exists(br_file):
                call(["brotli", "-d", br_file])

            dat_file = os.path.join(extract_tmp, f"{part}.new.dat")
            list_file = os.path.join(extract_tmp, f"{part}.transfer.list")
            img_file = os.path.join(img_tmp, f"{part}.img")

            if os.path.exists(dat_file) and os.path.exists(list_file):
                print(f"[{label}] Converting {part} dat to img...")
                Sdat2img(list_file, dat_file, img_file)
            elif os.path.exists(os.path.join(extract_tmp, f"{part}.img")):
                shutil.move(os.path.join(extract_tmp, f"{part}.img"), img_file)

            # Now Decompose the image so we can access files
            if os.path.exists(img_file):
                print(f"[{label}] Decomposing {part}.img...")
                extractor = imgextractor.Extractor()
                # Extractor.main(target, output_dir, work_dir)
                # It writes config to work_dir/config
                extractor.main(img_file, os.path.join(decomp_tmp, part), target_dir)

        return decomp_tmp
