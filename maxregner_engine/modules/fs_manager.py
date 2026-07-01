import os
import re

class FSMetadataManager:
    def __init__(self, base_fs_config, ui_fs_config):
        self.base_config = self._parse_config(base_fs_config)
        self.ui_config = self._parse_config(ui_fs_config)
        self.merged_config = {}

    def _parse_config(self, path):
        config = {}
        if not path or not os.path.exists(path): return config
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts: continue
                config[parts[0]] = parts[1:]
        return config

    def merge(self):
        all_paths = set(self.base_config.keys()) | set(self.ui_config.keys())
        for path in all_paths:
            if path in self.ui_config and path not in self.base_config:
                self.merged_config[path] = self.ui_config[path]
            elif path in self.base_config:
                self.merged_config[path] = self.base_config[path]

    def save(self, output_path):
        with open(output_path, 'w') as f:
            for path in sorted(self.merged_config.keys()):
                f.write(f"{path} {' '.join(self.merged_config[path])}\n")

class InitPatcher:
    def __init__(self, system_dir):
        self.system_dir = system_dir
        self.init_dir = os.path.join(system_dir, "etc", "init")

    def merge_service(self, source_rc):
        if not os.path.exists(source_rc): return
        with open(source_rc, 'r') as f:
            content = f.read()
        services = re.findall(r"(service\s+.*?\n(?:\s+.*?\n)*)", content)
        target_rc = os.path.join(self.init_dir, "maxregner_services.rc")
        os.makedirs(self.init_dir, exist_ok=True)
        with open(target_rc, 'a') as f:
            for svc in services:
                f.write(f"\n# Ported Service\n{svc}\n")
