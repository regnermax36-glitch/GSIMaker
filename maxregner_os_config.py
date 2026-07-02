# MaxRegnerOS Definition File
# Defines the boundaries of the "Purge and Build" logic.

CORE_WHITELIST = [
    "bin",
    "lib",
    "lib64",
    "etc",
    "framework",
    "usr",
    "fonts",
    "media/audio/ui"
]

PURGE_LIST = [
    "app",
    "priv-app",
    "system_ext",
    "product/app",
    "product/priv-app"
]

# MaxRegnerOS Proprietary Suite
MAXREGNER_APPS = [
    "MaxLauncher.apk",
    "MaxSettings.apk",
    "MaxSystemUI.apk"
]

MAXREGNER_OVERLAYS = [
    "MaxRegnerFrameworkOverlay.apk",
    "MaxRegnerSystemUIOverlay.apk",
    "MaxRegnerSettingsOverlay.apk"
]

BUILD_PROPS = {
    "ro.product.brand": "MaxRegner",
    "ro.product.model": "MaxRegnerOS Device",
    "ro.build.display.id": "MaxRegnerOS-v1.0-GENESIS",
    "ro.maxregner.version": "1.0",
    "ro.maxregner.ui": "MaxRegnerUI-v1",
    "ro.config.maxregner": "true"
}
