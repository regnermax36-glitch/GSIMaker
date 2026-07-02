#!/usr/bin/env python3
"""
  __  __   _   __  __ ___ ___ ___ _  _ ___ ___
 |  \/  | /_\  \ \/ / _ \ __/ __| \| | __| _ \
 | |\/| |/ _ \  >  <|   / _|| (_ | .` | _||   /
 |_|  |_/_/ \_\/_/\_\_|_\___|\___|_|\_|___|_|_\
                OS BUILDER V1.0
"""
import os
import sys
import shutil
import logging
from maxregner_engine.modules.extractor import AdvancedExtractor
from maxregner_os_config import CORE_WHITELIST, PURGE_LIST, BUILD_PROPS
from cgsi import repack_image, clean_up, IMG_DIR, decompose_images

class MaxRegnerOSBuilder:
    def __init__(self, lineage_zip: str):
        self.source_zip = lineage_zip
        self.work_dir = os.path.abspath("MAX_OS_WORK")
        self.output_img = "result_system.img"
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        self.logger = logging.getLogger("MaxRegnerOS")

    def initialize(self):
        self.logger.info("Initializing MaxRegnerOS Builder...")
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)
        os.makedirs(self.work_dir)
        clean_up(True)

    def build(self):
        self.initialize()
        extractor = AdvancedExtractor(self.work_dir)

        # 1. Extract and Decompose Source (LineageOS)
        self.logger.info("Extracting Source Core/Libs...")
        source_decomp_dir = extractor.extract_and_decompose(self.source_zip, "SOURCE")

        # 2. Setup Working Directory (IMG_DIR)
        shutil.copytree(source_decomp_dir, IMG_DIR, dirs_exist_ok=True)

        system_dir = os.path.join(IMG_DIR, "system", "system")
        if not os.path.exists(system_dir):
            system_dir = os.path.join(IMG_DIR, "system")

        # 3. THE PURGE: Remove non-core components
        self.logger.info("PURGE PHASE: Removing non-essential OS components...")
        for p in PURGE_LIST:
            target = os.path.join(system_dir, "..", p) # Handle system/system vs system
            if os.path.exists(target):
                shutil.rmtree(target)
                self.logger.info(f"  - Purged {p}")

        # 4. THE BUILD: Inject MaxRegnerOS Components
        self.logger.info("BUILD PHASE: Injecting MaxRegnerOS Suite...")

        # Overlays
        overlay_dir = os.path.join(system_dir, "product", "overlay")
        os.makedirs(overlay_dir, exist_ok=True)
        shutil.copytree("maxregner_os_assets/overlays", overlay_dir, dirs_exist_ok=True)

        # Apps
        app_dir = os.path.join(system_dir, "app")
        os.makedirs(app_dir, exist_ok=True)
        shutil.copytree("maxregner_os_assets/apps", app_dir, dirs_exist_ok=True)

        # Features (init scripts, etc.)
        shutil.copytree("maxregner_os_assets/features", system_dir, dirs_exist_ok=True)

        # 5. Branding
        self.logger.info("Applying MaxRegnerOS Identity...")
        prop_file = os.path.join(system_dir, "build.prop")
        if os.path.exists(prop_file):
            with open(prop_file, "a", encoding='utf-8') as f:
                f.write("\n# --- MaxRegnerOS GENESIS ---\n")
                for k, v in BUILD_PROPS.items():
                    f.write(f"{k}={v}\n")

        # 6. Repack
        self.logger.info("Repacking result_system.img...")
        os.environ["REPACK_FS"] = "ext"

        # Use config from source for repacking metadata
        source_config = os.path.join(self.work_dir, "SOURCE", "config")
        if os.path.exists(source_config):
            shutil.copytree(source_config, os.path.join(IMG_DIR, "config"), dirs_exist_ok=True)

        if repack_image(): return 1

        if os.path.exists(os.path.join(IMG_DIR, "out", "system.img")):
            shutil.move(os.path.join(IMG_DIR, "out", "system.img"), self.output_img)
            self.logger.info(f"SUCCESS: {self.output_img}")

        return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: maxregner_os_builder.py <lineage_rom.zip>")
        sys.exit(1)
    builder = MaxRegnerOSBuilder(sys.argv[1])
    sys.exit(builder.build())

if __name__ == "__main__":
    main()
