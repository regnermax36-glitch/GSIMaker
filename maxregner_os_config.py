# List of apps that can be safely removed without breaking the core system
SAFE_TO_PURGE = [
    "app/Browser",
    "app/Calculator",
    "app/Calendar",
    "app/Camera2",
    "app/DeskClock",
    "app/Email",
    "app/Gallery2",
    "app/Music",
    "app/Profiles",
    "app/Recorder",
    "priv-app/ExactCalculator",
    "priv-app/LineageParts",
    "priv-app/Updater"
]

BUILD_PROPS = {
    "ro.product.brand": "MaxRegner",
    "ro.product.model": "MaxRegnerOS",
    "ro.build.display.id": "MaxRegnerOS-GENESIS",
    "ro.maxregner.version": "1.0",
    "ro.config.maxregner": "true"
}
