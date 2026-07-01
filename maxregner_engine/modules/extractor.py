import os
import shutil
import subprocess
import zipfile
from cgsi import call, extract_partitions_from_payload, Sdat2img, gettype, imgextractor, IMG_DIR, tool_bin

class AdvancedExtractor:
    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def extract_and_decompose(self, rom_zip: str, label: str, selective=False):
        target_dir = os.path.join(self.work_dir, label)
        extract_tmp = os.path.join(target_dir, "EXTRACT")
        img_tmp = os.path.join(target_dir, "IMG")
        decomp_tmp = os.path.join(target_dir, "DECOMPOSED")
        os.makedirs(extract_tmp, exist_ok=True)
        os.makedirs(img_tmp, exist_ok=True)
        os.makedirs(decomp_tmp, exist_ok=True)

        print(f"[{label}] Selective Decompressing ZIP...")
        # 1. Faster: List zip content and only extract payload.bin or .new.dat files
        with zipfile.ZipFile(rom_zip, 'r') as z:
            names = z.namelist()
            targets = [n for n in names if 'payload.bin' in n or '.new.dat' in n or '.transfer.list' in n or (n.endswith('.img') and any(p in n for p in ['system', 'product', 'vendor', 'system_ext']))]
            for t in targets:
                z.extract(t, extract_tmp)

        parts = ['system', 'product', 'system_ext'] if selective else ['system', 'product', 'system_ext', 'vendor']

        payload = os.path.join(extract_tmp, "payload.bin")
        if os.path.exists(payload):
            print(f"[{label}] Selective Payload Extraction: {parts}")
            with open(payload, "rb") as f:
                extract_partitions_from_payload(f, parts, extract_tmp, 8)

        for part in parts:
            br_file = os.path.join(extract_tmp, f"{part}.new.dat.br")
            if os.path.exists(br_file):
                call(["brotli", "-d", br_file])

            dat_file = os.path.join(extract_tmp, f"{part}.new.dat")
            list_file = os.path.join(extract_tmp, f"{part}.transfer.list")
            img_file = os.path.join(img_tmp, f"{part}.img")

            if os.path.exists(dat_file) and os.path.exists(list_file):
                Sdat2img(list_file, dat_file, img_file)
            elif os.path.exists(os.path.join(extract_tmp, f"{part}.img")):
                shutil.move(os.path.join(extract_tmp, f"{part}.img"), img_file)

            if os.path.exists(img_file):
                file_type = gettype(img_file)
                if file_type == 'sparse':
                    unsparse_img = img_file + ".raw"
                    call(["simg2img", img_file, unsparse_img])
                    os.remove(img_file)
                    shutil.move(unsparse_img, img_file)
                    file_type = gettype(img_file)

                out_path = os.path.join(decomp_tmp, part)
                if file_type == 'ext':
                    extractor = imgextractor.Extractor()
                    extractor.main(img_file, out_path, target_dir)
                elif file_type == 'erofs':
                    call(["extract.erofs", "-i", img_file, "-o", decomp_tmp, "-x"], out_=False)

                os.remove(img_file)

        return decomp_tmp
