from setuptools import setup, find_packages
from os import path
import re

with open("README.md") as f:
    long_description = f.read()


def find_version():
    init_file = open(path.join(path.dirname(__file__), 'voiager', '__init__.py')).read()
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", init_file, re.M)
    if version:
        return version.group(1)
    raise RuntimeError("Cannot find version in __init__.py")


setup(
    name='Voiager',
    version=find_version(),
    packages=find_packages(exclude=['docs','catalogs','results']),
    url='https://github.com/nhamaus/Voiager',
    license='MIT',
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Programming Language :: Python :: 3",
    ],
    author='Nico Hamaus',
    author_email='nhamaus@gmail.com',
    description='Perform cosmological analyses using voids identified in large-scale structure survey data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'voiager = voiager.__main__:main'
        ],
    },
    install_requires=[
        'astropy',
        'cython',
        'emcee',
        'getdist',
        'h5py',
        'healpy',
        'matplotlib',
        'numpy',
        'pyabel',
        'pyyaml',
        'scipy',
        'tqdm',
        'vide',
    ],
)