from setuptools import find_packages, setup

setup(name='pylogging',
      version='0.2.0',
      description='File logging for Python',
      author='Ankur Srivastava',
      author_email='best.ankur@gmail.com',
      url='https://github.com/ansrivas/pylogging',
      download_url='https://github.com/ansrivas/pylogging/tarball/0.2.0',
      license='MIT',
      install_requires=['future', 'requests', 'requests-futures'],
      packages=find_packages())
