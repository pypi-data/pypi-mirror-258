from setuptools import setup, find_packages

setup(
    name='lsl_xdf_reader',
    version='0.1',
    packages=find_packages(),
    description='A package for reading and parsing Lab Streaming Layer (lsl) xdf data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Bartu Atabek',
    author_email='batabek@metu.edu.tr',
    url='https://github.com/metu-humate/lsl-xdf-data-reader',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
    ],
    keywords=['xdf data reader', 'lsl data reader', 'xdf', 'lsl', 'lab streaming layer', 'xdf reader', 'lsl reader'],
)