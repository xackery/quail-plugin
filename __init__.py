import os
import auto_load
import tomllib

PACKAGE_NAME = __package__
PACKAGE_PATH = os.path.dirname(__file__)


with open(os.path.join(PACKAGE_PATH, "blender_manifest.toml"), "rb") as f:
    import tomllib

    manifest = tomllib.load(f)
    QUAIL_TOOLS_VERSION = manifest["version"]

# auto_load.init(PACKAGE_NAME)


def register():
    import bpy

    from . import handlers

    auto_load.register()

    handlers.QuailHandlers.register()


def unregister():
    import bpy

    from . import handlers

    handlers.QuailHandlers.unregister()

    auto_load.unregister()


if __name__ == "__main__":
    register()
