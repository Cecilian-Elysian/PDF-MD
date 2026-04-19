import sys
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import fitz
from paddleocr import PaddleOCR


app = FastAPI()

ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)


def convert_pdf_to_markdown(pdf_path):
    doc = fitz.open(pdf_path)
    md_content = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")

        result = ocr.ocr(img_data, cls=True)

        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                md_content.append(text)

        md_content.append("")

    return "\n".join(md_content)


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("app/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    temp_pdf = "temp_upload.pdf"
    with open(temp_pdf, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        markdown_content = convert_pdf_to_markdown(temp_pdf)
    finally:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)

    return {"markdown": markdown_content}