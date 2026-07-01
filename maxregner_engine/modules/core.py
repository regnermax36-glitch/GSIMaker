import os
import shutil
import logging

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
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                # Use move for UI source components if we don't need them anymore,
                # but copy is safer if ui_img_dir is reused.
                # Given we want speed, we use move.
                shutil.move(src, dst)

    def merge_product(self):
        ui_product = os.path.join(self.ui_dir, "product")
        out_product = os.path.join(self.out_dir, "product") # Corrected path
        if not os.path.exists(os.path.dirname(out_product)):
            out_product = os.path.join(os.path.dirname(self.out_dir), "product")

        if os.path.exists(ui_product):
            self.logger.info("Porting product partition...")
            if os.path.exists(out_product):
                shutil.rmtree(out_product)
            shutil.move(ui_product, out_product)
