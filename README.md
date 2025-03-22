# FontAwesome Converter

<div align="center">

![FontAwesome Converter](https://img.shields.io/badge/FontAwesome-Converter-blue?style=for-the-badge&logo=font-awesome)

**Convert FontAwesome icons to PNG format**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

[English](README.md) | [中文](README_CN.md)

</div>

## Overview

FontAwesome Converter is a Python tool that allows you to convert FontAwesome icons to PNG format with flexible options. The tool supports both SVG-based and font-based rendering methods and can generate icons in multiple sizes simultaneously.

## Features

- **Multiple Rendering Methods**: Convert using SVG or font-based rendering
- **Flexible Size Options**: Generate icons in multiple preset sizes (16px to 512px)
- **Style Support**: Convert icons in solid, regular, or brands styles
- **Color Customization**: Apply custom colors to your icons
- **Organized Output**: Automatically organizes icons by size in separate folders
- **Batch Processing**: Convert individual icons or the entire icon set
- **Logging Control**: Adjustable verbosity with multiple log levels

## Installation

```bash
# Clone the repository
git clone https://github.com/SakuraPuare/fontawesome-converter.git
cd fontawesome-converter

# Install the package
pip install -e .
```

## Usage

### Command Line Interface

Convert a single icon:

```bash
fontawesome-convert convert arrow-right /path/to/fontawesome --style solid --size 512 --color "#FF0000"
```

Convert all icons:

```bash
fontawesome-convert convert-all /path/to/fontawesome --style solid --size 512
```

### Options

- `--style`: Icon style (solid, regular, brands)
- `--size`: Maximum output size in pixels (will generate all standard sizes up to this value)
- `--color`: Color for the icon (as hex code)
- `--render-method`: Method to use for rendering (svg or font)
- `--output-dir`: Directory to save the outputs
- `--log-level`: Set logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Python API

```python
from fontawesome_converter import FontAwesomeConverter

# Initialize converter
converter = FontAwesomeConverter("/path/to/fontawesome")

# Convert a single icon
converter.convert_svg("arrow-right", style="solid", size=512, color="#FF0000")

# Convert all icons
converter.convert_all(style="solid", size=512, render_method="svg")
```

## Output Structure

Converted icons are organized in the following structure:

```
output/
  16px/
    icon1_solid.png
    icon2_regular.png
    ...
  24px/
    icon1_solid.png
    icon2_regular.png
    ...
  32px/
    ...
  48px/
    ...
  64px/
    ...
  128px/
    ...
  256px/
    ...
  512px/
    ...
```

## Examples

Convert an icon to multiple sizes (maximum 512px):

```bash
fontawesome-convert convert arrow-right /path/to/fontawesome
```

Convert all "solid" style icons to blue PNGs:

```bash
fontawesome-convert convert-all /path/to/fontawesome --style solid --color "#0000FF"
```

Adjust log level for detailed information:

```bash
fontawesome-convert --log-level DEBUG convert arrow-right /path/to/fontawesome
```

## Requirements

- Python 3.10+
- FontAwesome files (can be downloaded from [FontAwesome](https://fontawesome.com/))
- Dependencies: cairosvg, Pillow, loguru, click, tqdm

## License

This project is licensed under the MIT License - see the LICENSE file for details. 