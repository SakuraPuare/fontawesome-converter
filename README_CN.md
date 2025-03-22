# FontAwesome Converter

<div align="center">

![FontAwesome Converter](https://img.shields.io/badge/FontAwesome-Converter-blue?style=for-the-badge&logo=font-awesome)

**将 FontAwesome 图标转换为 PNG 格式**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

[English](README.md) | [中文](README_CN.md)

</div>

## 概述

FontAwesome Converter 是一个 Python 工具，可以将 FontAwesome 图标转换为 PNG 格式，并提供灵活的选项。该工具支持基于 SVG 和基于字体的渲染方法，可以同时生成多种尺寸的图标。

## 特点

- **多种渲染方法**：支持 SVG 和基于字体的渲染
- **灵活的尺寸选项**：可以生成多种预设尺寸的图标（16px 至 512px）
- **样式支持**：支持转换 solid、regular 或 brands 样式的图标
- **颜色自定义**：可以为图标应用自定义颜色
- **输出组织**：自动按尺寸将图标组织到单独的文件夹中
- **批量处理**：可以转换单个图标或整个图标集
- **日志控制**：可调节的日志级别，支持多种详细程度

## 安装

```bash
# 克隆仓库
git clone https://github.com/SakuraPuare/fontawesome-converter.git
cd fontawesome-converter

# 安装包
pip install -e .
```

## 使用方法

### 命令行界面

转换单个图标：

```bash
fontawesome-convert convert arrow-right /path/to/fontawesome --style solid --size 512 --color "#FF0000"
```

转换所有图标：

```bash
fontawesome-convert convert-all /path/to/fontawesome --style solid --size 512
```

### 选项

- `--style`：图标样式（solid、regular、brands）
- `--size`：最大输出尺寸（将生成所有标准尺寸，直到该值）
- `--color`：图标颜色（十六进制代码）
- `--render-method`：渲染方法（svg 或 font）
- `--output-dir`：保存输出的目录
- `--log-level`：设置日志详细程度（DEBUG、INFO、WARNING、ERROR、CRITICAL）

### Python API

```python
from fontawesome_converter import FontAwesomeConverter

# 初始化转换器
converter = FontAwesomeConverter("/path/to/fontawesome")

# 转换单个图标
converter.convert_svg("arrow-right", style="solid", size=512, color="#FF0000")

# 转换所有图标
converter.convert_all(style="solid", size=512, render_method="svg")
```

## 输出结构

转换后的图标将按以下结构组织：

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

## 示例

将一个图标转换为多种尺寸（最大 512px）：

```bash
fontawesome-convert convert arrow-right /path/to/fontawesome
```

将所有"solid"样式的图标转换为蓝色 PNG：

```bash
fontawesome-convert convert-all /path/to/fontawesome --style solid --color "#0000FF"
```

调整日志级别以获取详细信息：

```bash
fontawesome-convert --log-level DEBUG convert arrow-right /path/to/fontawesome
```

## 要求

- Python 3.10+
- FontAwesome 文件（可以从 [FontAwesome](https://fontawesome.com/) 下载）
- 依赖项：cairosvg, Pillow, loguru, click, tqdm

## 许可证

本项目使用 MIT 许可证 - 详情请查看 LICENSE 文件。 