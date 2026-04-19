import sys
import os
from paddleocr import PaddleOCR
from fitz import fitz

def convert_pdf_to_md(pdf_path, output_path=None):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return

    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + ".md"

    print(f"Converting: {pdf_path}")

    ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)
    doc = fitz.open(pdf_path)

    md_content = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"Processing page {page_num + 1}/{len(doc)}...")

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")

        result = ocr.ocr(img_data, cls=True)

        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                md_content.append(text)

        md_content.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

    print(f"Done! Output: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    convert_pdf_to_md(pdf_path)