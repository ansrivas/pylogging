import re
from codecs import open  # To use a consistent encoding
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    with open('pylogging/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


setup(name='pylogging',
      version=get_version(),
      description='File logging for Python',
      long_description=long_description,
      author='Ankur Srivastava',
      author_email='best.ankur@gmail.com',
      url='https://github.com/ansrivas/pylogging',
      download_url='https://github.com/ansrivas/pylogging/tarball/{0}'.format(get_version()),
      include_package_data=True,
      license='MIT',
      zip_safe=False,
      install_requires=['future', 'requests-futures', 'ujson==4.0.0', 'graypy==2.1.0'],
      extras_require={
          'dev': [
              'pytest',
              'pytest-pep8',
              'pytest-cov',
              'python-language-server[all]'
          ]
      },
      classifiers=[
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6", ],
      packages=find_packages())
