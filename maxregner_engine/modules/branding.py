import os

class BrandingEngine:
    def __init__(self, system_dir: str):
        self.system_dir = system_dir

    def patch_build_prop(self):
        prop_file = os.path.join(self.system_dir, "build.prop")
        if not os.path.exists(prop_file):
            return

        print("[BrandingEngine] Patching build.prop...")
        with open(prop_file, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.startswith("ro.build.display.id="):
                line = "ro.build.display.id=MaxRegnerUI-v2.0-ULTRA\n"
            elif line.startswith("ro.product.model="):
                line = "ro.product.model=MaxRegner Ultra\n"
            new_lines.append(line)

        new_lines.append("\n# MaxRegnerUI Branding\n")
        new_lines.append("ro.maxregnerui.version=2.0\n")
        new_lines.append("ro.config.maxregnerui=true\n")

        with open(prop_file, 'w') as f:
            f.writelines(new_lines)
