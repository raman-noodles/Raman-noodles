from setuptools import setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(name='ramannoodles',
      version='1.0',
      description='A python package for analyzing raman spectroscopy data.',
      url='https://github.com/raman-noodles/Raman-noodles',
      author='Raman Noodles Group, University of Washington (2019)',
#       long_description=long_description,
#       long_description_content_type="text/markdown",
      license='MIT',
      packages=['ramannoodles'],
      install_requires=['numpy', 'jcamp', 'requests', 'matplotlib', 'scipy', 'lmfit', 'peakutils'])
