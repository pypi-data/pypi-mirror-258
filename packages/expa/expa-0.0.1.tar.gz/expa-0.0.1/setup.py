import pathlib
import re
import setuptools


def parse_version(filename):
  text = (pathlib.Path(__file__).parent / filename).read_text()
  version = re.search(r"__version__ = '(.*)'", text).group(1)
  return version


setuptools.setup(
    name='expa',
    version=parse_version('expa/__init__.py'),
    author='Jurgis Pasukonis',
    author_email='jurgisp@gmail.com',
    # url='https://github.com/jurgisp/expa',
    license='Apache 2.0',
    description='Metric logging and analysis for ML experiments',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.9',
    # install_requires=parse_reqs()[0],
    # extras_require=parse_reqs()[1],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
