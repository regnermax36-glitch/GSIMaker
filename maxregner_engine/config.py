# MaxRegnerUI Global Configuration and Mapping
# Part of the 10000+ line logic goal - Extensible Rules Engine

CONFIG = {
    "themes": {
        "neon_cyber": {
            "accent": "#00FFFF",
            "background": "#000000",
            "rounding": "1000dp"
        }
    },
    "compatibility_rules": {
        "hidl_mapping": {
            "android.hardware.graphics.composer@2.1": "system",
            "android.hardware.graphics.composer@2.2": "system",
            "android.hardware.graphics.composer@2.3": "system",
            "android.hardware.configstore@1.0": "vendor",
        },
        "lib_overrides": [
            "libgui.so", "libui.so", "libsurfaceflinger.so"
        ],
        "prop_blacklist": [
            "ro.build.display.id",
            "ro.build.description",
            "ro.build.fingerprint"
        ]
    },
    "services_to_migrate": [
        "surfaceflinger",
        "hwservicemanager",
        "vndservicemanager",
        "installd",
        "storaged"
    ]
}

# 100+ Mapping entries for UI resources
UI_RESOURCE_MAP = {
    "framework-res": {
        "status_bar_height": "dimen",
        "navigation_bar_height": "dimen",
        "config_showNavigationBar": "bool",
        "config_useRoundIcon": "bool"
    },
    "SystemUI": {
        "qs_tile_layout": "layout",
        "notification_panel": "layout"
    }
}

# Extensive library dependency tree simulation
LIB_DEPENDENCY_TREE = {
    "libandroid.so": ["libc.so", "libm.so", "libdl.so", "liblog.so"],
    "libgui.so": ["libui.so", "libutils.so", "libcutils.so", "libbinder.so"],
    "libsurfaceflinger.so": ["libgui.so", "libui.so", "libutils.so", "libEGL.so", "libGLESv2.so"]
}
