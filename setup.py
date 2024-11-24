#!/usr/bin/env python3

# To build Mailnagger run this script:
# ./setup.py build
# Then to install Mailnagger run pip as root:
# pip install --break-system-packages .

from setuptools import setup, Command, find_packages
from distutils.command.install_data import install_data
from setuptools.command.build import build

import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig


# NOTE: These should be in sync with Mailnag.common.dist_cfg PACKAGE_NAME
#       and APP_VERSION.
PACKAGE_NAME = 'mailnagger'
APP_VERSION = '2.3.0.dev0'


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


class Uninstall(Command):
    def run(self):
        # TODO
        pass


setup(name=PACKAGE_NAME,
    version=APP_VERSION,
    description='An extensible mail notification daemon',
    author='Timo Kankare',
    author_email='timo.kankare@iki.fi',
    url='https://github.com/tikank/mailnagger',
    license='GNU GPL2',
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
            "mailnagger = mailnagger:main",
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
    install_requires = [
        'pygobject',
        'pyxdg',
        'dbus-python',
    ],
    cmdclass={
        'build': BuildData,
        'install_data': InstallData,
        'uninstall': Uninstall
    }
)
