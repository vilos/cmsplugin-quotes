from setuptools import setup, find_packages

import cmsplugin_quotes
version = cmsplugin_quotes.__version__

setup(
    name = 'cmsplugin-quotes',
    version = version,
    description = 'a rotating quotes plugin for django-cms',
    author = 'Viliam Segeda',
    author_email = 'viliam.segeda@gmail.com',
    packages = find_packages(),
    zip_safe=False,
    install_requires = [
        'django-taggit',
    ],
)