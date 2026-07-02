#!/usr/bin/env python3
"""
  __  __   _   __  __ ___ ___ ___ _  _ ___ ___
 |  \/  | /_\  \ \/ / _ \ __/ __| \| | __| _ \
 | |\/| |/ _ \  >  <|   / _|| (_ | .` | _||   /
 |_|  |_/_/ \_\/_/\_\_|_\___|\___|_|\_|___|_|_\
                MAXREGNERUI OS BUILDER
"""
import os
import sys
import shutil
import logging
import time
import subprocess
from maxregner_engine.modules.extractor import FastExtractor
from maxregner_os_config import SAFE_TO_PURGE, BUILD_PROPS
from cgsi import repack_image, clean_up, IMG_DIR

class OSBuilder:
    def __init__(self, lineage_zip):
        self.source_zip = lineage_zip
        self.work_dir = os.path.abspath("MAX_OS_WORK")
        self.output_img = "result_system.img"
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        self.logger = logging.getLogger("MaxRegnerUI")

    def build(self):
        start = time.time()
        if os.path.exists(self.work_dir): shutil.rmtree(self.work_dir)
        os.makedirs(self.work_dir)
        clean_up(True)

        extractor = FastExtractor(self.work_dir)
        source_dir = extractor.extract_and_decompose(self.source_zip, "SOURCE")

        self.logger.info("Setting up system...")
        os.makedirs(IMG_DIR, exist_ok=True)
        for part in os.listdir(source_dir):
            shutil.move(os.path.join(source_dir, part), os.path.join(IMG_DIR, part))

        sys_root = os.path.join(IMG_DIR, "system", "system")
        if not os.path.exists(sys_root): sys_root = os.path.join(IMG_DIR, "system")

        self.logger.info("Surgical Purge of LineageOS bloat...")
        for p in SAFE_TO_PURGE:
            target = os.path.join(sys_root, p)
            if os.path.exists(target):
                subprocess.run(["rm", "-rf", target])
            else:
                # check system_root/.. as well for product/system_ext
                target = os.path.join(sys_root, "..", p)
                if os.path.exists(target): subprocess.run(["rm", "-rf", target])

        self.logger.info("Injecting MaxRegnerUI Redesign...")
        overlay_dir = os.path.join(sys_root, "product", "overlay")
        os.makedirs(overlay_dir, exist_ok=True)
        shutil.copy("MaxRegnerOSMaster.apk", overlay_dir)

        prop_file = os.path.join(sys_root, "build.prop")
        if os.path.exists(prop_file):
            with open(prop_file, "a") as f:
                f.write("\n# MaxRegnerOS Branding\n")
                for k, v in BUILD_PROPS.items(): f.write(f"{k}={v}\n")

        self.logger.info("Final Repack...")
        os.environ["REPACK_FS"] = "ext"
        config_src = os.path.join(self.work_dir, "SOURCE", "config")
        if os.path.exists(config_src):
            shutil.copytree(config_src, os.path.join(IMG_DIR, "config"), dirs_exist_ok=True)

        if repack_image(): return 1

        if os.path.exists(os.path.join(IMG_DIR, "out", "system.img")):
            shutil.move(os.path.join(IMG_DIR, "out", "system.img"), self.output_img)
            self.logger.info(f"DONE! Total time: {time.time()-start:.2f}s")
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    sys.exit(OSBuilder(sys.argv[1]).build())
