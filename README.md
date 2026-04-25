# PDF-MD

将 PDF 转换为 Markdown 格式的工具，基于 PaddleOCR 实现高准确度中文识别。

## 功能特性

- 📄 **PDF 转 Markdown** - 提取文本并保留基本格式
- 🔤 **中文 OCR** - 基于 PaddleOCR 的中文识别支持
- 🌐 **Web 界面** - FastAPI 驱动的简洁上传界面
- 🐳 **Docker 部署** - 一键容器化部署
- 📦 **CLI 工具** - 命令行快速转换

## 支持格式

| 输入 | 输出 |
|------|------|
| PDF 文件 | Markdown (.md) |

## 安装

### 方式一：pip 安装

```bash
pip install -r requirements.txt
```

### 方式二：Docker

```bash
docker build -t pdf-md .
docker run -p 8000:8000 pdf-md
```

### 依赖说明

- **fastapi** - Web 框架
- **uvicorn[standard]** - ASGI 服务器
- **python-multipart** - 文件上传支持
- **paddlepaddle** - OCR 引擎
- **paddleocr** - OCR 工具库
- **PyMuPDF** - PDF 处理

## 使用

### 命令行模式

```bash
python convert.py <pdf_path> [output_path]
```

**参数说明：**
- `pdf_path` - PDF 文件路径（必需）
- `output_path` - 输出 Markdown 路径（可选，默认与 PDF 同名）

**示例：**
```bash
# 转换单个文件
python convert.py input.pdf

# 指定输出路径
python convert.py input.pdf output.md
```

### Web 服务模式

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 上传 PDF 文件进行转换。

### API 接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | Web 界面 |
| `/convert` | POST | 上传 PDF 并转换 |

**请求示例：**
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/convert
```

## 配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 文件大小限制 | 50MB | 最大上传文件大小 |
| OCR 语言 | ch | 识别语言，中文为 `ch` |

## 项目结构

```
PDF-MD/
├── README.md           # 说明文档
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 配置
├── convert.py          # CLI 转换工具
└── app/
    ├── main.py         # FastAPI 服务
    └── templates/
        └── index.html  # Web 界面
```

## 故障排除

**Q: OCR 识别效果不理想？**
A: 确保 PaddlePaddle 已正确安装，可参考 [PaddleOCR 官方文档](https://github.com/PaddlePaddle/PaddleOCR)。

**Q: Docker 部署内存不足？**
A: 建议分配 4GB 以上内存给 Docker 容器。

## 许可证

MIT