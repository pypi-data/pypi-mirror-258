from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'PyCloud serves to operate different cloud providers'

setup(
  name="pycloudops", 
  version=VERSION,
  author="Endrit Berisha",
  author_email="endritpb@gmail.com",
  description=DESCRIPTION,
  packages=find_packages(),
  install_requires=[], 
  keywords=['python', 'cloud', 'operations', 'path'],
  classifiers= [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
  ]
)
