# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

"""Support to get various resources."""

import sysconfig
import xdg.BaseDirectory as base

from importlib.resources import files
from importlib.resources.abc import Traversable
from Mailnag.common.dist_cfg import PACKAGE_NAME, DATA_DIR, PLUGIN_DIR
from pathlib import Path
from types import ModuleType


def get_data_paths() -> list[Path]:
    """Returns paths to mailnagger data files."""
    data_paths = []
    data_paths.append(DATA_DIR)
    # Add "./data" in workdir for running from builddir
    data_paths.append(Path("./data"))
    data_paths.extend(Path(p) for p in base.load_data_paths(PACKAGE_NAME))
    return data_paths


def get_data_file(filename: str) -> Path | None:
    """Return path to filename if it exists anywhere in the data paths,
       else return None
    """

    data_paths = get_data_paths()

    for direc in data_paths:
        file_path = direc / filename
        if file_path.exists():
            return file_path
    return None


def get_icon_paths() -> list[Path]:
    """Returns paths to icon files."""
    data_paths = []
    data_paths.append(Path(sysconfig.get_path("data")) / "share" / "icons")
    # Add "./data" in workdir for running from builddir
    data_paths.append(Path("./data/icons"))
    data_paths.extend(Path(p) / "icons" for p in base.load_data_paths(PACKAGE_NAME))
    return data_paths


def get_config_path() -> Path:
    cfg_folder = Path(base.xdg_config_home) / "mailnag"
    return cfg_folder


def get_plugin_paths() -> list[Path | Traversable]:
    """Returns paths to plugin directories."""
    PLUGIN_LIB_PATH = PLUGIN_DIR
    PLUGIN_USER_PATH = get_config_path() / "plugins"
    return [
        PLUGIN_LIB_PATH,
        PLUGIN_USER_PATH
    ]


def get_resource_text(module: ModuleType, resource: str) -> str:
    """Returns resource text from module."""
    return files(module).joinpath(resource).read_text()

