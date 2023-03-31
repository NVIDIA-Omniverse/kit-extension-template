import os
import platform
import packmanapi


def get_host_platform() -> str:
    """Get host platform string (platform-arch, E.g.: "windows-x86_64")"""
    arch = platform.machine()
    if arch == "AMD64":
        arch = "x86_64"
    platform_host = platform.system().lower() + "-" + arch
    return platform_host


if __name__ == "__main__":
    TOOLS_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
    kit_dep_file = os.path.join(TOOLS_ROOT, "deps/kit-sdk.packman.xml")
    packmanapi.pull(kit_dep_file, tokens={"config": "release", "platform": get_host_platform()})

