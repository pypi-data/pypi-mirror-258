from setuptools import setup, find_packages

setup(
    name='colordithering',
    version='0.1',
    packages=find_packages(),
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