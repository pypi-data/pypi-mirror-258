#!/usr/bin/env python3

from setuptools import setup
from pathlib import Path

setup(
    name='filewrap',
    version='1.1.7',
    py_modules=['filewrap'],
    license='MIT',
    description='Python package for file/directory/archive management.',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/filewrap-os',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux'],
    python_requires='>=3.6'
)

# - Update README.md
# - Update Version Number
# - Tar Wrap the Package: python setup.py sdist
# - Check Package: twine check dist/*
# - Upload to PYPI: twine upload dist/* -u __token__ -p pypi-<Token Value>
# - Commit Changes
# - Change Release Version in Github Repo