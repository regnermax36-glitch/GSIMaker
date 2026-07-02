import os
import shutil
import subprocess
import zipfile
from cgsi import call, extract_partitions_from_payload, Sdat2img, gettype, imgextractor, IMG_DIR, tool_bin

class FastExtractor:
    def __init__(self, work_dir):
        self.work_dir = work_dir

    def extract_and_decompose(self, rom_zip, label):
        target = os.path.join(self.work_dir, label)
        ext_tmp = os.path.join(target, "EXTRACT")
        img_tmp = os.path.join(target, "IMG")
        decomp = os.path.join(target, "DECOMP")
        os.makedirs(ext_tmp, exist_ok=True)
        os.makedirs(img_tmp, exist_ok=True)
        os.makedirs(decomp, exist_ok=True)

        print(f"[{label}] Fast Decompressing ZIP...")
        subprocess.run(["unzip", "-q", rom_zip, "-d", ext_tmp])

        payload = os.path.join(ext_tmp, "payload.bin")
        if os.path.exists(payload):
            with open(payload, "rb") as f:
                extract_partitions_from_payload(f, ['system', 'product'], ext_tmp, 16)

        for part in ['system', 'product']:
            img_file = os.path.join(img_tmp, f"{part}.img")
            src_img = os.path.join(ext_tmp, f"{part}.img")
            if os.path.exists(src_img):
                shutil.move(src_img, img_file)

            if os.path.exists(img_file):
                file_type = gettype(img_file)
                if file_type == 'sparse':
                    call(["simg2img", img_file, img_file + ".raw"])
                    os.remove(img_file)
                    os.rename(img_file + ".raw", img_file)
                    file_type = gettype(img_file)

                out_path = os.path.join(decomp, part)
                os.makedirs(out_path, exist_ok=True)

                if file_type == 'ext':
                    # Use imgextractor to preserve metadata
                    extractor = imgextractor.Extractor()
                    extractor.main(img_file, out_path, target)
                elif file_type == 'erofs':
                    call(["extract.erofs", "-i", img_file, "-o", decomp, "-x"], out_=False)

                os.remove(img_file)
        return decomp
