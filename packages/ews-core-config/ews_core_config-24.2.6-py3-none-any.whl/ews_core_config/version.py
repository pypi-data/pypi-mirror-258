__all__ = ("VERSION", "version_info")

VERSION = "24.2.6"


def version_info() -> str:
    """
    Show the version info

    Example:
        ```python
        import ews_core_config

        print(ews_core_config.version_info())
        ```

    """
    import platform
    import sys
    from importlib import import_module  # noqa: F401
    from pathlib import Path

    optional_deps = []

    info = {
        "ews_core_config version": VERSION,
        "install path": Path(__file__).resolve().parent,
        "python version": sys.version,
        "platform": platform.platform(),
        "optional deps. installed": optional_deps,
    }
    return "\n".join("{:>30} {}".format(k + ":", str(v).replace("\n", " ")) for k, v in info.items())
