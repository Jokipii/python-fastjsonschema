#!/usr/bin/env python
import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    LONG_DESCRIPTION = readme.read()

# Get the version string. Cannot be done with import!
# https://packaging.python.org/en/latest/single_source_version.html
try:
    execfile('fastjsonschema/version.py')
except NameError:
    with open(os.path.join('fastjsonschema', 'version.py'), 'rt') as version_file:
        VERSION_GLOBALS = {}
        # pylint: disable=exec-used
        exec(version_file.read(), VERSION_GLOBALS)
        __version__ = VERSION_GLOBALS['__version__']


setup(
    name='fastjsonschema',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'requests',
        'jsonpointer',
        'email_validator',
        'rfc3987',
        'expynent',
        'Click',
    ],
    extras_require={
        'devel': [
            'colorama',
            'jsonschema',
            'json-spec',
            'pylint',
            'pytest',
            'pytest-cache',
            'validictory',
            'pydocstyle',
            'pytest-benchmark',
        ],
    },
    entry_points='''
        [console_scripts]
        fastjsonschema=fastjsonschema.__main__:main
    ''',
    url='https://github.com/seznam/python-fastjsonschema',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    description='Fastest Python implementation of JSON schema',
    long_description=LONG_DESCRIPTION,
    license='BSD',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
