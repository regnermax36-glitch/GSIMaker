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
        """
        Merge UI components from UI source into Base system.
        Strategy: Keep Base /system/lib* (for kernel/vendor compat),
        replace /system/priv-app, /system/app, /system/framework from UI.
        """
        self.logger.info("Merging system components...")

        ui_system = os.path.join(self.ui_dir, "system", "system")
        if not os.path.exists(ui_system):
            ui_system = os.path.join(self.ui_dir, "system") # fallback

        components = ["app", "priv-app", "framework", "etc/sysconfig", "etc/permissions"]

        for comp in components:
            src = os.path.join(ui_system, comp)
            dst = os.path.join(self.out_dir, comp)
            if os.path.exists(src):
                self.logger.info(f"  - Porting {comp}")
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst, symlinks=True)

    def merge_product(self):
        ui_product = os.path.join(self.ui_dir, "product")
        out_product = os.path.join(self.out_dir, "..", "product") # assuming out_dir is system/system
        if os.path.exists(ui_product):
            self.logger.info("Porting product partition...")
            if os.path.exists(out_product):
                shutil.rmtree(out_product)
            shutil.copytree(ui_product, out_product, symlinks=True)
