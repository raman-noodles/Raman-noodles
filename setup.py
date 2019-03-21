from setuptools import setup

setup(name='ramannoodles',
      version='1.0',
      description='A python package for analyzing raman spectroscopy data.',
      url='https://github.com/raman-noodles/Raman-noodles',
      author='Raman Noodles Group, University of Washington (2019)',
      license='MIT',
      packages=['ramannoodles'],
      install_requires=['numpy', 'jcamp', 'requests', 'matplotlib', 'scipy', 'lmfit', 'peakutils'])
