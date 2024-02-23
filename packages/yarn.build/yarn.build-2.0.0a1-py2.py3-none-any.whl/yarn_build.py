"""zest.releaser plugin to build JavaScript projects"""
import logging
import subprocess
import sys
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

from zest.releaser.utils import ask

logger = logging.getLogger("yarn.build")


def get_configured_location(path):
    setup_cfg = path / "setup.cfg"
    if setup_cfg.exists():
        config = ConfigParser()
        config.read(setup_cfg)
        try:
            folder_path = Path(config.get("yarn.build", "folder"))
            if folder_path.exists():
                return folder_path
            logger.warning(f"{folder_path} does not exist")
        except NoSectionError:
            pass
        except (NoOptionError, ValueError):
            logger.warning(
                "No valid `folder` option found in `yarn.build` section "
                "within setup.cfg"
            )

    return None


def find_package_json(path):
    location = get_configured_location(path)
    if location:
        return location
    return recursive_find_package_json(path)


def recursive_find_package_json(path):
    """Find a `packages.json` file and run yarn on it"""
    for file_obj in path.iterdir():
        if file_obj.name == "package.json":
            logger.info("yarn: package.json found!")
            return path
        elif file_obj.is_dir():
            recursive_find_package_json(file_obj)

    return None


def build(path):
    """Build the JavaScript project at the given location"""
    logger.debug("yarn: Compile dependencies")
    subprocess.call(
        [
            "yarn",
            "--frozen-lockfile",
        ],
        cwd=path,
    )
    logger.debug("yarn: Build the project")
    subprocess.call(
        [
            "yarn",
            "run",
            "release",
        ],
        cwd=path,
    )


def build_project(data):
    """Build a JavaScript project from a zest.releaser tag directory"""
    tagdir = data.get("tagdir")
    if not tagdir:
        msg = "yarn: no tagdir found in data."
        logger.warn(msg)
        return
    logger.debug(f"yarn: Find and build JavaScript projects on {tagdir}")
    try:
        location = find_package_json(Path(tagdir))
        if location:
            build(location)
    except Exception:  # noqa: B902
        logger.warn(
            "yarn: Building the project failed.",
            exc_info=True,
        )
        if data:
            # We were called as an entry point of zest.releaser.
            if not ask("Error building JS project. Do you want to continue?"):
                sys.exit(1)
