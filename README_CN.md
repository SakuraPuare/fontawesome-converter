# FontAwesome Converter

<div align="center">

![FontAwesome Converter](https://img.shields.io/badge/FontAwesome-Converter-blue?style=for-the-badge&logo=font-awesome)

**将 FontAwesome 图标转换为 PNG 格式**

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![SVG](https://img.shields.io/badge/SVG-Supported-orange?style=flat-square&logo=svg)
![PNG](https://img.shields.io/badge/PNG-Generator-yellow?style=flat-square&logo=image)
[![PyPI version](https://img.shields.io/pypi/v/fontawesome-converter.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/fontawesome-converter/)
[![PyPI downloads](https://img.shields.io/pypi/dm/fontawesome-converter.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/fontawesome-converter/)

[English](README.md) | [中文](README_CN.md)

</div>

<p align="center">
  <img src="https://img.fortawesome.com/349cfdf6/fa-free-logo.svg" alt="FontAwesome 图标" width="600" />
</p>

## 📋 概述

FontAwesome Converter 是一个 Python 工具，可以将 FontAwesome 图标转换为 PNG 格式，并提供灵活的选项。该工具支持基于 SVG 和基于字体的渲染方法，可以同时生成多种尺寸的图标。

## ✨ 特点

- 🎨 **多种渲染方法**：支持 SVG 和基于字体的渲染
- 📐 **灵活的尺寸选项**：可以生成多种预设尺寸的图标（16px 至 512px）
- 🔣 **样式支持**：支持转换 solid、regular 或 brands 样式的图标
- 🎭 **颜色自定义**：可以为图标应用自定义颜色
- 📁 **输出组织**：自动按尺寸将图标组织到单独的文件夹中
- 🔄 **批量处理**：可以转换单个图标或整个图标集
- 📊 **日志控制**：可调节的日志级别，支持多种详细程度

## 🚀 安装

### 从 PyPI 安装（推荐）

```bash
pip install fontawesome-converter
```

### 从源代码安装

```bash
# 克隆仓库
git clone https://github.com/SakuraPuare/fontawesome-converter.git
cd fontawesome-converter

# 安装包
pip install -e .
```

## 📖 使用方法

### 📂 FontAwesome 路径要求

`/path/to/fontawesome` 参数应指向从 [fontawesome.com/download](https://fontawesome.com/download) 下载并解压后的 FontAwesome 包目录。下载 ZIP 文件后，请解压缩并使用解压后的目录路径。

<details>
<summary>预期目录结构</summary>

```
fontawesome-directory/
├── css/
├── js/
├── svgs/
│   ├── solid/
│   ├── regular/
│   └── brands/
├── webfonts/
└── metadata/
    └── icons.json
```
</details>

> **重要说明：**
> - 确保使用解压后的目录路径，而不是 ZIP 文件
> - 工具需要访问 `svgs/` 目录进行 SVG 渲染，以及 `webfonts/` 进行字体渲染
> - 两种渲染方法都需要 `metadata/icons.json` 文件
> - 支持 FontAwesome 的免费版和专业版

### 💻 命令行界面

转换单个图标：

```bash
fa-convert convert arrow-right /path/to/fontawesome --style solid --size 512 --color "#FF0000"
```

转换所有图标：

```bash
fa-convert convert-all /path/to/fontawesome --style solid --size 512
```

### ⚙️ 选项

| 选项 | 描述 |
|--------|-------------|
| `--style` | 图标样式（solid、regular、brands） |
| `--size` | 最大输出尺寸（将生成所有标准尺寸，直到该值） |
| `--color` | 图标颜色（十六进制代码） |
| `--render-method` | 渲染方法（svg 或 font） |
| `--output-dir` | 保存输出的目录 |
| `--log-level` | 设置日志详细程度（DEBUG、INFO、WARNING、ERROR、CRITICAL） |

### 🐍 Python API

```python
from fontawesome_converter import FontAwesomeConverter

# 初始化转换器
converter = FontAwesomeConverter("/path/to/fontawesome")

# 转换单个图标
converter.convert_svg("arrow-right", style="solid", size=512, color="#FF0000")

# 转换所有图标
converter.convert_all(style="solid", size=512, render_method="svg")
```

## 📊 输出结构

转换后的图标将按以下结构组织：

<details>
<summary>查看输出目录结构</summary>

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
</details>

## 🔍 示例

<details open>
<summary><b>基本用法</b></summary>

将一个图标转换为多种尺寸（最大 512px）：

```bash
fa-convert convert arrow-right /path/to/fontawesome
```
</details>

<details>
<summary><b>自定义颜色</b></summary>

将所有"solid"样式的图标转换为蓝色 PNG：

```bash
fa-convert convert-all /path/to/fontawesome --style solid --color "#0000FF"
```
</details>

<details>
<summary><b>详细日志</b></summary>

调整日志级别以获取详细信息：

```bash
fa-convert --log-level DEBUG convert arrow-right /path/to/fontawesome
```
</details>

## 🔧 要求

- Python 3.11+
- FontAwesome 文件（可以从 [FontAwesome](https://fontawesome.com/download) 下载）
- 依赖项：
  - cairosvg - 用于 SVG 渲染
  - Pillow - 用于图像处理
  - loguru - 用于增强日志
  - click - 用于命令行界面
  - tqdm - 用于进度条显示

## 📜 许可证

本项目使用 MIT 许可证 - 详情请查看 LICENSE 文件。

---

<div align="center">
  <sub>由 SakuraPuare 用 ❤️ 构建</sub>
</div> 