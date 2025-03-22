"""Setup script for FontAwesome Converter."""

from setuptools import setup, find_packages

setup(
    name="fontawesome-converter",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "loguru>=0.6.0",
        "tqdm>=4.60.0",
        "cairosvg>=2.5.0",
        "Pillow>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "fa-convert=fontawesome_converter.cli:cli",
        ],
    },
    author="SakuraPuare",
    author_email="sakurapuare@sakurapuare.com",
    description="Convert FontAwesome icons to PNG format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SakuraPuare/fontawesome-converter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
) 