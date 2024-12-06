#!/usr/bin/env python3

# To build Mailnagger run this script:
# ./setup.py build
# Then to install Mailnagger run pip as root:
# pip install --break-system-packages .

from setuptools import setup, find_packages
from distutils.command.install_data import install_data
from setuptools.command.build import build

import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig


this_directory = Path(__file__).parent

# NOTE: These should be in sync with Mailnag.common.dist_cfg PACKAGE_NAME
#       and APP_VERSION.
PACKAGE_NAME = 'mailnagger'
app_version = (this_directory / "VERSION").read_text().strip()

long_description = (this_directory / "README.md").read_text()

logger = logging.getLogger(__name__)

# TODO : This hack won't work with --user and --home options
PREFIX = sysconfig.get_path('data')
for arg in sys.argv:
    if arg.startswith('--prefix='):
        PREFIX = arg[9:]

BUILD_DIR = 'build'
for arg in sys.argv:
    if arg.startswith('--build-base='):
        BUILD_DIR = arg[13:]

BUILD_LOCALE_DIR = os.path.join(BUILD_DIR, 'locale')
BUILD_PATCH_DIR = os.path.join(BUILD_DIR, 'patched')
INSTALL_LIB_DIR = os.path.join(sysconfig.get_path('purelib'), 'Mailnag')


class BuildData(build):
    def run(self):
        # generate translations
        try:
            rc = subprocess.call('./gen_locales ' + BUILD_LOCALE_DIR, shell = True)
            if (rc != 0):
                if (rc == 1): err = "MKDIR_ERR"
                elif (rc == 2): err = "MSGFMT_ERR"
                else: err = "UNKNOWN_ERR"
                raise Warning("gen_locales returned %d (%s)" % (rc, err))
        except Exception as e:
            logger.error("Building locales failed.")
            logger.error("Error: %s" % str(e))
            sys.exit(1)

        # remove patch dir (if existing)
        shutil.rmtree(BUILD_PATCH_DIR, ignore_errors = True)
        Path(BUILD_PATCH_DIR).mkdir(parents=True, exist_ok=True)

        # patch paths
        self._patch_file(
            './data/mailnagger.desktop',
            os.path.join(BUILD_PATCH_DIR, 'mailnagger.desktop'),
            '/usr',
            PREFIX
        )
        self._patch_file(
            './data/mailnagger-config.desktop',
            os.path.join(BUILD_PATCH_DIR, 'mailnagger-config.desktop'),
            '/usr',
            PREFIX
        )
        build.run(self)


    def _patch_file(self, infile, outfile, orig, replaced):
        with open(infile, 'r') as f:
            strn = f.read()
            strn = strn.replace(orig, replaced)
        with open(outfile, 'w') as f:
            f.write(strn)


class InstallData(install_data):
    def run(self):
        self._add_locale_data()
        self._add_icon_data()
        install_data.run(self)


    def _add_locale_data(self):
        for root, dirs, files in os.walk(BUILD_LOCALE_DIR):
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(
                    'share/locale',
                    os.path.dirname(src_path[len(BUILD_LOCALE_DIR)+1:])
                )
                self.data_files.append((dst_path, [src_path]))

    def _add_icon_data(self):
        for root, dirs, files in os.walk('data/icons'):
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(
                    'share/icons',
                    os.path.dirname(src_path[len('data/icons')+1:])
                )
                self.data_files.append((dst_path, [src_path]))


setup(name=PACKAGE_NAME,
    version=app_version,
    description='An extensible mail notification daemon',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Timo Kankare',
    author_email='timo.kankare@iki.fi',
    project_urls={
        "homepage": "https://github.com/tikank/mailnagger",
        "source": "https://github.com/tikank/mailnagger",
        "issues": "https://github.com/tikank/mailnagger/issues",
        "releasenotes": "https://github.com/tikank/mailnagger/blob/master/NEWS",
        "documentation": "https://github.com/tikank/mailnagger/tree/master/docs",
    },
    license='GPL-2.0-or-later',
    license_file='LICENSE',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: GTK",
        "Environment :: X11 Applications :: Gnome",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: English",
        "Natural Language :: Finnish",
        "Natural Language :: German",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Communications :: Email",
        "Topic :: Communications :: Email :: Post-Office :: IMAP",
        "Topic :: Communications :: Email :: Post-Office :: POP3",
        "Topic :: Utilities",
    ],
    packages=find_packages(
        include=[
            "Mailnag*",
            "mailnagger*"
        ]
    ) + ["Mailnag.plugins"],
    package_data = {
        'Mailnag.configuration.ui' : [
            'account_widget.ui',
            'config_window.ui',
        ],
        'Mailnag.configuration.desktop': [
            'mailnagger.desktop',
        ],
    },
    entry_points={
        "console_scripts": [
            "mailnagger = mailnagger.daemon:main",
            "mailnagger-config = mailnagger.config:main",
        ],
    },
    data_files=[
        ('share/mailnagger', ['data/mailnag.ogg']),
        ('share/mailnagger', ['data/mailnag.png']),
        ('share/man/man1', ['data/mailnagger.1', 'data/mailnagger-config.1']),
        ('share/metainfo', ['data/mailnag.appdata.xml']),
        ('share/applications', [
                os.path.join(BUILD_PATCH_DIR, 'mailnagger.desktop'),
                os.path.join(BUILD_PATCH_DIR, 'mailnagger-config.desktop')
        ])
    ],
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        'pygobject',
        'pyxdg',
        'dbus-python',
        "importlib_resources;python_version<'3.11'",
    ],
    extras_require={
        "dev": [
            "pygobject-stubs",
            "types-pyxdg",
            "pytest",
            "nox",
            "types-setuptools",
        ],
    },
    cmdclass={
        'build': BuildData,
        'install_data': InstallData,
    }
)
