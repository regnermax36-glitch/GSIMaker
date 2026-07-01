import os
import shutil

class BlobHealer:
    def __init__(self, system_dir: str, donor_system_dir: str):
        self.system_dir = system_dir
        self.donor_system_dir = donor_system_dir
        self.lib_paths = ["lib64", "lib", "system_ext/lib64", "system_ext/lib"]

    def heal_all(self):
        print("[BlobHealer] Healing system binaries...")
        essential_libs = ["libhidlbase.so", "libhidltransport.so", "libhwbinder.so"]

        for lib in essential_libs:
            target_found = False
            for lp in self.lib_paths:
                if os.path.exists(os.path.join(self.system_dir, lp, lib)):
                    target_found = True
                    break

            if not target_found:
                self._pull_from_donor(lib)

    def _pull_from_donor(self, lib: str):
        for lp in self.lib_paths:
            src = os.path.join(self.donor_system_dir, lp, lib)
            if os.path.exists(src):
                dst = os.path.join(self.system_dir, lp)
                os.makedirs(dst, exist_ok=True)
                print(f"  [Healer] Restoring {lib} from donor to {lp}")
                shutil.copy(src, dst)
                return
