# PDF-MD

将 PDF 转换为 Markdown 格式的工具，基于 PaddleOCR 实现中文识别。

## 功能特性

- PDF 转 Markdown 文本提取
- 中文 OCR 识别支持
- FastAPI Web 界面
- Docker 部署支持

## 安装

```bash
pip install -r requirements.txt
```

## 使用

### 命令行

```bash
python convert.py <pdf_path>
```

### Web 服务

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 上传 PDF 文件。

## Docker 部署

```bash
docker build -t pdf-md .
docker run -p 8000:8000 pdf-md
```

## 依赖

- fastapi
- uvicorn[standard]
- python-multipart
- paddlepaddle
- paddleocr
- PyMuPDF

## 配置

- 文件大小限制：50MB
- 支持中文 (lang='ch')
