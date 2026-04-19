import sys
import os
import fitz
from paddleocr import PaddleOCR


def convert_pdf_to_markdown(pdf_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    result = convert_pdf_to_markdown(pdf_path)
    print(result)