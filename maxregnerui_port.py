#!/usr/bin/env python3
import os
import sys
import shutil
from src import imgextractor
from src.contextpatch import main as contextpatch
from src.fspatch import main as fspatch
from src.gettype import gettype
from cgsi import extract_rom, extract_images, decompose_images, repack_image, clean_up, IMG_DIR, EXTRACT_DIR, call

def inject_overlay():
    print("- Injecting MaxRegnerUI Redesign Overlay")
    product_overlay_dir = os.path.join(IMG_DIR, "system", "system", "product", "overlay")
    os.makedirs(product_overlay_dir, exist_ok=True)
    shutil.copy("MaxRegnerUIOverlay.apk", product_overlay_dir)

    # Update build.prop
    build_prop = os.path.join(IMG_DIR, "system", "system", "build.prop")
    if os.path.exists(build_prop):
        with open(build_prop, "a", encoding='utf-8') as f:
            f.write("\n# MaxRegnerUI Redesign\n")
            f.write("ro.maxregnerui.version=1.0\n")
            f.write("ro.config.maxregnerui=true\n")
            f.write("ro.product.model=LineageOS MaxRegnerUI\n")
    return 0

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <lineage_rom.zip>")
        return 1

    rom_zip = sys.argv[1]
    if not os.path.exists(rom_zip):
        print(f"Error: {rom_zip} not found.")
        return 1

    clean_up(True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    print("Step 1: Extracting ROM...")
    if extract_rom(rom_zip): return 1

    print("Step 2: Extracting Images...")
    if extract_images(): return 1

    print("Step 3: Decomposing Images...")
    if decompose_images(): return 1

    print("Step 4: Injecting MaxRegnerUI...")
    if inject_overlay(): return 1

    print("Step 5: Repacking Image...")
    os.environ["REPACK_FS"] = "ext"
    if repack_image(): return 1

    if os.path.exists(os.path.join(IMG_DIR, "out", "system.img")):
        shutil.move(os.path.join(IMG_DIR, "out", "system.img"), "result_system.img")
        print("Success! Result saved as result_system.img")

    clean_up()
    return 0

if __name__ == "__main__":
    main()
