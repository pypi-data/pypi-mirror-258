#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Colav.
# Distributed under the terms of the Modified BSD License.

# -----------------------------------------------------------------------------
# Minimal Python version sanity check (from IPython)
# -----------------------------------------------------------------------------

# See https://stackoverflow.com/a/26737258/2268280
# sudo pip3 install twine
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
# For test purposes
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

from __future__ import print_function
from setuptools import setup, find_packages

import os
import sys
import codecs


v = sys.version_info


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


shell = False
if os.name in ('nt', 'dos'):
    shell = True
    warning = "WARNING: Windows is not officially supported"
    print(warning, file=sys.stderr)


def main():
    setup(
        # Application name:
        name="Kahi_impactu",

        # Version number (initial):
        version=get_version('kahi_impactu/_version.py'),

        # Application author details:
        author="Colav",
        author_email="colav@udea.edu.co",

        # Packages
        packages=find_packages(exclude=['tests']),

        # Include additional files into the package
        include_package_data=True,

        # Details
        url="https://github.com/colav/Kahi_plugins",
        #
        license="BSD",

        description="Kahi impactu metapackage to install all plugins for impactu ETL",

        long_description=open("README.md").read(),

        long_description_content_type="text/markdown",

        # Dependent packages (distributions)
        # put you packages here
        install_requires=[
            'kahi==0.0.5a0',
            'Kahi_doaj_sources==0.1.1-beta',
            'Kahi_minciencias_opendata_affiliations==0.1.1-beta',
            'Kahi_minciencias_opendata_person==0.1.1-beta',
            'Kahi_openalex_affiliations==0.1.1-beta',
            'Kahi_openalex_person==0.1.1-beta',
            'Kahi_openalex_sources==0.1.1-beta',
            'Kahi_openalex_subjects==0.1.1-beta',
            'Kahi_openalex_works==0.1.5-beta',
            'Kahi_ranking_udea_works==0.1.2-beta',
            'Kahi_ror_affiliations==0.1.2-beta',
            'Kahi_scholar_works==0.1.3-beta',
            'Kahi_scienti_affiliations==0.1.3-beta',
            'Kahi_scienti_person==0.1.3-beta',
            'Kahi_scienti_sources==0.1.2-beta',
            'Kahi_scienti_works==0.1.4-beta',
            'Kahi_scimago_sources==0.1.0-beta',
            'Kahi_scopus_works==0.1.3-beta',
            'Kahi_staff_udea_affiliations==0.1.1-beta',
            'Kahi_staff_udea_person==0.1.1-beta',
            'Kahi_wos_works==0.1.3-beta',
        ],
    )


if __name__ == "__main__":
    main()
