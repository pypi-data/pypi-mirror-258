from setuptools import setup

setup(
    name='coloraura',
    version='1.0.1',
    description='A Python module for text styling with color and gradient support',
    long_description='''# ColorAura

ColorAura is a Python module for text styling with color and gradient support.

## Features

- Apply colors to text using ANSI escape codes.
- Create gradients with customizable start and end colors.
- Add text styles such as bold, italic, and strikethrough.
- Supports all standard ANSI colors.
- Hex color support for custom colors.

## Installation

You can install ColorAura using pip:

```
pip install coloraura
```

## Usage

Here's a simple example demonstrating how to use ColorAura to style text:

```python
from coloraura import color, gradient, style

# Apply red color to text
red_text = color.style("Hello, ColorAura!", color='red')
print(red_text)

# Apply a blue-to-green gradient to text
gradient_text = gradient.style("Hello, Gradient!", gradient=('blue', 'green'))
print(gradient_text)

# Apply bold style to text
bold_text = style.style("Hello, Bold!", style='bold')
print(bold_text)
```

## License

ColorAura is released under the GNU General Public License (GPLv3). See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on GitHub.''',
    long_description_content_type='text/markdown',
    url='https://github.com/visuallysynced/coloraura',
    author='Your Name',
    license='GPLv3',
    packages=['coloraura']
)


