#!/usr/bin/env python

import copy

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildCmd(build_py):
    def run(self):
        # build foris plugin files
        from foris_plugins_distutils import build
        cmd = build(copy.copy(self.distribution))
        cmd.ensure_finalized()
        cmd.run()

        # build package
        build_py.run(self)


setup(
    name="Foris Storage Plugin",
    version="1.1",
    description="Storage plugin for foris web interfce",
    author="CZ.NIC, z. s. p. o.",
    author_email="stepan.henek@nic.cz",
    url="https://gitlab.labs.nic.cz/turris/foris-storage-plugin/",
    license="GPL-3.0",
    requires=[
        "foris",
    ],
    setup_requires=[
        'babel',
        'jinja2',
        'libsass',
        'foris_plugins_distutils',
    ],
    provides=[
        "foris_plugins.storage",
    ],
    packages=[
        "foris_plugins.storage",
    ],
    package_data={
        '': [
            "templates/**",
            "templates/**/*",
            "templates/javascript/**",
            "templates/javascript/**/*",
            "locale/**/LC_MESSAGES/*.mo",
            "static/css/*.css",
            "static/fonts/*",
            "static/img/*",
            "static/js/*.js",
            "static/js/contrib/*",
        ],
    },
    cmdclass={
        "build_py": BuildCmd,  # modify build_py to build the foris files as well
    }
)