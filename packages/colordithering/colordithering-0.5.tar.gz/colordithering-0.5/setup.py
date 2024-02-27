from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='colordithering',
    version='0.5',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = [
        "colorama>=0.4.6"
    ],
    author='ingobeans',
    description='Color strings using ANSI escape codes. Uses "dithering" to attempt to match the specified RGB value as close as possible.',
    url='https://github.com/ingobeans/terminal-rgb-color-dithering',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)