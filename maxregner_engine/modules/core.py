import os
import shutil
import logging
import subprocess

class MergeEngine:
    def __init__(self, base_img_dir: str, ui_img_dir: str, output_system_dir: str):
        self.base_dir = base_img_dir
        self.ui_dir = ui_img_dir
        self.out_dir = output_system_dir
        self.logger = logging.getLogger("MergeEngine")

    def merge_system_components(self):
        self.logger.info("Merging system components...")

        ui_system = os.path.join(self.ui_dir, "system", "system")
        if not os.path.exists(ui_system):
            ui_system = os.path.join(self.ui_dir, "system")

        components = ["app", "priv-app", "framework", "etc/sysconfig", "etc/permissions"]

        for comp in components:
            src = os.path.join(ui_system, comp)
            dst = os.path.join(self.out_dir, comp)
            if os.path.exists(src):
                self.logger.info(f"  - Porting {comp}")
                # Fast delete using rm -rf
                if os.path.exists(dst):
                    subprocess.run(["rm", "-rf", dst])
                shutil.move(src, dst)

    def merge_product(self):
        ui_product = os.path.join(self.ui_dir, "product")
        out_product = os.path.join(self.out_dir, "product")
        if not os.path.exists(os.path.dirname(out_product)):
            out_product = os.path.join(os.path.dirname(self.out_dir), "product")

        if os.path.exists(ui_product):
            self.logger.info("Porting product partition...")
            if os.path.exists(out_product):
                subprocess.run(["rm", "-rf", out_product])
            shutil.move(ui_product, out_product)
