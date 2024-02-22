__author__ = "Derek Moody"
from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.1"
LICENSE = "LGPL-3.0"

DESC = "🔊 Play music and sounds in your Python scripts"

README = Path('README.md').read_text()


setup(
  name='minisound',
  version=VERSION,
  description=DESC,
  long_description=README,
  long_description_content_type="text/markdown",
  author=__author__,
  license=LICENSE,
  packages=find_packages(exclude=[]),
  zip_safe=False,
  install_requires=['playsound', 'boombox', 'anyio', 'sniffio', 'idna',],
  python_requires='>=3.6',
  include_package_data=True,
  package_data={'minisound': ['assets/*']},
)
