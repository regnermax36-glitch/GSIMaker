import os

class CompatPatcher:
    def __init__(self, system_dir: str):
        self.system_dir = system_dir

    def fix_linker_configs(self):
        etc_dir = os.path.join(self.system_dir, "etc")
        if not os.path.exists(etc_dir): return
        for file in os.listdir(etc_dir):
            if file.startswith("ld.config.") and file.endswith(".txt"):
                self._patch_ld_config(os.path.join(etc_dir, file))

    def _patch_ld_config(self, path: str):
        print(f"[CompatPatcher] Patching {os.path.basename(path)}")
        with open(path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if "namespace.default.searchpaths" in line:
                line = line.strip() + ":/system/product/lib64:/system/product/lib\n"
            new_lines.append(line)

        with open(path, 'w') as f:
            f.writelines(new_lines)
