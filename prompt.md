创建一个 python pypi 包，用于将 fontawesome 的图标转成 png 格式。要求如下

1. 使用 click 来创建 cli，要求使用的 arg 有 size 控制生成的文件大小，color 控制生成的图标颜色，渲染方式使用 svg 渲染还是字体文件渲染。路径读取下载的 fontawesome 文件解压后的路径
2. 使用 loguru 进行彩色 log，tqdm 进行进度条监控
3. 要能支持多种渲染方式 下载的文件有 webfonts 和 svg。对于 svg 直接渲染，对于 webfonts 使用字体渲染

可以使用 metadata/icons.json 内的内容，里面有所有的配置

部分内容如下

```icons.json
{
  "0": {
    "changes": [
      "6.0.0-beta1",
      "6.2.0",
      "6.3.0",
      "6.4.0",
      "6.5.0",
      "6.6.0",
      "6.7.0"
    ],
    "ligatures": [],
    "search": {
      "terms": [
        "Digit Zero",
        "nada",
        "none",
        "zero",
        "zilch"
      ]
    },
    "styles": [
      "solid"
    ],
    "unicode": "30",
    "label": "0",
    "voted": false,
    "svg": {
      "solid": {
        "last_modified": 1717164890,
        "raw": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 320 512\"><path d=\"M0 192C0 103.6 71.6 32 160 32s160 71.6 160 160l0 128c0 88.4-71.6 160-160 160S0 408.4 0 320L0 192zM160 96c-53 0-96 43-96 96l0 128c0 53 43 96 96 96s96-43 96-96l0-128c0-53-43-96-96-96z\"/></svg>",
        "viewBox": [
          0,
          0,
          320,
          512
        ],
        "width": 320,
        "height": 512,
        "path": "M0 192C0 103.6 71.6 32 160 32s160 71.6 160 160l0 128c0 88.4-71.6 160-160 160S0 408.4 0 320L0 192zM160 96c-53 0-96 43-96 96l0 128c0 53 43 96 96 96s96-43 96-96l0-128c0-53-43-96-96-96z"
      }
    },
    "free": [
      "solid"
    ]
  },
```

解压后的文件结构如下 分为 web 版本 和 desktop 版本

```web
├── css
├── js
├── less
├── metadata
├── scss
├── sprites
├── svgs
│   ├── brands
│   ├── regular
│   └── solid
└── webfonts
```

```desktop
❯ tree -d
.
├── metadata
├── otfs
└── svgs
    ├── brands
    ├── regular
    └── solid

7 directories```