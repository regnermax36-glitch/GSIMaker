#!/usr/bin/env python3
"""
  __  __   _   __  __ ___ ___ ___ _  _ ___ ___
 |  \/  | /_\  \ \/ / _ \ __/ __| \| | __| _ \
 | |\/| |/ _ \  >  <|   / _|| (_ | .` | _||   /
 |_|  |_/_/ \_\/_/\_\_|_\___|\___|_|\_|___|_|_\
                PRO ENGINE V2.0
"""
import os
import sys
import shutil
import logging
from maxregner_engine.modules.core import MergeEngine
from maxregner_engine.modules.compat_patcher import CompatPatcher
from maxregner_engine.modules.branding import BrandingEngine
from maxregner_engine.modules.extractor import AdvancedExtractor
from maxregner_engine.modules.healer import BlobHealer
from cgsi import repack_image, clean_up, IMG_DIR, decompose_images

class MaxRegnerPro:
    def __init__(self, base_rom: str, ui_rom: str):
        self.base_rom = base_rom
        self.ui_rom = ui_rom
        self.work_dir = os.path.abspath("MAX_PRO_WORK")
        self.output_img = "result_system.img"
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        self.logger = logging.getLogger("MaxRegnerPro")

    def initialize(self):
        self.logger.info("Initializing MaxRegner Pro Engine...")
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)
        os.makedirs(self.work_dir)
        clean_up(True)

    def process(self):
        self.initialize()
        extractor = AdvancedExtractor(self.work_dir)

        # 1. Extract and Decompose Base ROM
        base_decomp_dir = extractor.extract_and_decompose(self.base_rom, "BASE")

        # 2. Extract and Decompose UI Source ROM
        ui_decomp_dir = extractor.extract_and_decompose(self.ui_rom, "UI_SOURCE")

        # 3. Setup Working directory (IMG_DIR) for final assembly
        self.logger.info("Setting up base partitions for modification...")
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        shutil.copytree(base_decomp_dir, IMG_DIR, dirs_exist_ok=True)

        # Determine system directory
        system_dir = os.path.join(IMG_DIR, "system", "system")
        if not os.path.exists(system_dir):
            system_dir = os.path.join(IMG_DIR, "system")

        # 4. Merge UI components from UI source
        ui_system_src = os.path.join(ui_decomp_dir, "system", "system")
        if not os.path.exists(ui_system_src):
            ui_system_src = os.path.join(ui_decomp_dir, "system")

        merger = MergeEngine(base_decomp_dir, ui_decomp_dir, system_dir)
        merger.merge_system_components()
        merger.merge_product()

        # 5. Compatibility & Healing
        patcher = CompatPatcher(system_dir)
        patcher.fix_linker_configs()

        healer = BlobHealer(system_dir, ui_system_src)
        healer.heal_all()

        branding = BrandingEngine(system_dir)
        branding.patch_build_prop()

        # 6. Inject custom overlays
        self.inject_overlays(system_dir)

        # 7. Repack
        self.logger.info("Repacking result_system.img...")
        os.environ["REPACK_FS"] = "ext"

        # We need the config files from the base extraction for repack
        base_config = os.path.join(self.work_dir, "BASE", "config")
        if os.path.exists(base_config):
            shutil.copytree(base_config, os.path.join(IMG_DIR, "config"), dirs_exist_ok=True)

        if repack_image():
            return 1

        if os.path.exists(os.path.join(IMG_DIR, "out", "system.img")):
            shutil.move(os.path.join(IMG_DIR, "out", "system.img"), self.output_img)
            self.logger.info(f"SUCCESS: {self.output_img}")

        return 0

    def inject_overlays(self, system_dir):
        # Product partition might be in IMG_DIR/product or inside system_dir/product depending on merge
        product_overlay = os.path.join(system_dir, "product", "overlay")
        if not os.path.exists(os.path.dirname(product_overlay)):
             product_overlay = os.path.join(IMG_DIR, "product", "overlay")

        os.makedirs(product_overlay, exist_ok=True)
        for apk in ["MaxRegnerFrameworkOverlay.apk", "MaxRegnerSystemUIOverlay.apk", "MaxRegnerSettingsOverlay.apk"]:
            if os.path.exists(apk):
                shutil.copy(apk, product_overlay)

def main():
    if len(sys.argv) < 3:
        print("Usage: maxregner_pro.py <base_rom.zip> <ui_source_rom.zip>")
        sys.exit(1)

    engine = MaxRegnerPro(sys.argv[1], sys.argv[2])
    sys.exit(engine.process())

if __name__ == "__main__":
    main()
