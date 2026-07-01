#!/usr/bin/env python3
import os
import sys
import shutil
from cgsi import extract_rom, extract_images, decompose_images, repack_image, clean_up, IMG_DIR, EXTRACT_DIR, call

# Define Overlays to inject
OVERLAYS = [
    "MaxRegnerFrameworkOverlay.apk",
    "MaxRegnerSystemUIOverlay.apk",
    "MaxRegnerSettingsOverlay.apk"
]

def apply_maxregner_branding():
    print(">>> Applying MaxRegnerUI Global Branding <<<")

    # 1. Inject Overlays
    product_overlay_dir = os.path.join(IMG_DIR, "system", "system", "product", "overlay")
    os.makedirs(product_overlay_dir, exist_ok=True)
    for apk in OVERLAYS:
        if os.path.exists(apk):
            print(f"  - Injected {apk}")
            shutil.copy(apk, product_overlay_dir)
        else:
            print(f"  - Warning: {apk} not found!")

    # 2. Advanced build.prop Tweaks
    build_prop = os.path.join(IMG_DIR, "system", "system", "build.prop")
    if os.path.exists(build_prop):
        print("  - Patching build.prop")
        with open(build_prop, "a", encoding='utf-8') as f:
            f.write("\n# --- MaxRegnerUI Redesign Edition ---\n")
            f.write("ro.maxregnerui.version=2.0_ULTRA\n")
            f.write("ro.maxregnerui.codename=NEON_CYBER\n")
            f.write("ro.config.maxregnerui=true\n")
            f.write("ro.product.model=LineageOS MaxRegnerUI Edition\n")
            f.write("ro.product.brand=MaxRegner\n")
            f.write("ro.product.name=MaxRegnerUI\n")
            # UI Tweaks
            f.write("persist.sys.theme.accent=neon_cyan\n")
            f.write("ro.config.hw_quickview=true\n")
            f.write("debug.hwui.renderer=skiavk\n") # Performance tweak
            f.write("ro.surface_flinger.max_frame_buffer_acquired_buffers=3\n")

    # 3. Branding for About Page (if possible via file replacement or prop)
    return 0

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <lineage_rom.zip>")
        return 1

    rom_zip = sys.argv[1]
    if not os.path.exists(rom_zip):
        print(f"Error: {rom_zip} not found.")
        return 1

    print("========================================")
    print("    MAXREGNER-UI PORTING MASTER TOOL    ")
    print("========================================")

    clean_up(True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    print("[1/5] Extracting Source ROM...")
    if extract_rom(rom_zip): return 1

    print("[2/5] Partition Extraction...")
    if extract_images(): return 1

    print("[3/5] Image Decomposition...")
    if decompose_images(): return 1

    print("[4/5] Redesigning UI...")
    if apply_maxregner_branding(): return 1

    print("[5/5] Repacking Master Image...")
    os.environ["REPACK_FS"] = "ext"
    if repack_image(): return 1

    if os.path.exists(os.path.join(IMG_DIR, "out", "system.img")):
        shutil.move(os.path.join(IMG_DIR, "out", "system.img"), "result_system.img")
        print("\nSUCCESS! MaxRegnerUI GSI created: result_system.img")

    clean_up()
    return 0

if __name__ == "__main__":
    main()
