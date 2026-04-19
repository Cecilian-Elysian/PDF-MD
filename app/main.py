import sys
import os
import uuid
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import fitz
from paddleocr import PaddleOCR


app = FastAPI()

MAX_FILE_SIZE = 50 * 1024 * 1024

ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)


def convert_pdf_to_markdown(pdf_path):
    doc = fitz.open(pdf_path)
    md_content = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")

        result = ocr.ocr(img_data, cls=True)

        if result and result is not None:
            for line_result in result:
                if line_result:
                    for line in line_result:
                        if line and len(line) >= 2:
                            text = line[1][0] if isinstance(line[1], (list, tuple)) else line[1]
                            md_content.append(text)

        md_content.append("")

    return "\n".join(md_content)


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("app/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="文件大小超过限制（最大 50MB）")

    temp_pdf = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
            f.write(content)
            temp_pdf = f.name

        markdown_content = convert_pdf_to_markdown(temp_pdf)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}")
    finally:
        if temp_pdf and os.path.exists(temp_pdf):
            os.remove(temp_pdf)

    return {"markdown": markdown_content}