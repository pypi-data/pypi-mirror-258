from setuptools import setup, find_packages

desc = """A package to color text with ANSI escape codes, but takes in an RGB value and uses dithering to try match it.

The colorize_text function accepts a string and a RGB tuple. It returns the colorized string.
To see the package in use you can try the run_example function.

Example usage:
```python
import colordithering

text = '''
███████████████████████████████████
██████████ Hello World! ███████████
███████████████████████████████████
'''

color = (255, 125, 0) # orange color
print(colordithering.colorize_text(text, color))

```"""

setup(
    name='colordithering',
    version='0.6',
    packages=find_packages(),
    long_description=desc,
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