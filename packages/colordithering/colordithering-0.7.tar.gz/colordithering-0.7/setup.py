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

```


The `return_array` parameter of colorize_text will return a 2D array of each character rather than a string. The values in each cell will be a dict, with the keys `text` and `color`. 
Text will be the character. Color will be the ANSI escape code.

Example usage with return_array:
```python
import colordithering

text = '''
███████████████████████████████████
██████████ Hello World! ███████████
███████████████████████████████████
'''

color = (255, 125, 0) # orange color

colorized = colordithering.colorize_text(text, color, True) # set return_array to True

for y in range(len(colorized)):
    for x in range(len(colorized[y])):
        character_at_cell = colorized[y][x]["text"]
        color_at_cell = colorized[y][x]["color"]

        print(color_at_cell + character_at_cell, end="") 
        # print the ANSI escape code first to set the color, then the character.
        # the end="" makes it so python doesn't print a new line automatically
    
    print() # new line

```"""

setup(
    name='colordithering',
    version='0.7',
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