# app/ocr_demo.py  (verbose)
from pdf2image import convert_from_path, pdfinfo_from_path
import pytesseract
import sys, traceback, os

def main(pdf_path):
    try:
        print('SCRIPT START')
        print('PDF path:', pdf_path)
        if not os.path.exists(pdf_path):
            print(f'File not found: {pdf_path}')
            return

        poppler_path = r"D:\invoice-extractor\poppler\poppler-25.11.0\Library\bin"
        print('Using poppler_path =', poppler_path)

        # print pdf info (uses pdftoppm/pdftotext behind the scenes)
        try:
            info = pdfinfo_from_path(pdf_path, poppler_path=poppler_path)
            print('pdfinfo:', info)
        except Exception as e:
            print('pdfinfo_from_path FAILED:', repr(e))

        # ensure pytesseract path if present
        tesseract_candidate = r"D:\orc\tesseract.exe"
        if os.path.exists(tesseract_candidate):
            pytesseract.pytesseract.tesseract_cmd = tesseract_candidate
            print('Using pytesseract.tesseract_cmd =', tesseract_candidate)
        else:
            print('tesseract candidate not found at', tesseract_candidate)
            print('pytesseract will use PATH fallback')

        # Convert pages (this is where pdftoppm is invoked)
        print('Calling convert_from_path...')
        pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        print('convert_from_path returned', len(pages), 'pages')

        # Save first page as debug image so we can inspect
        debug_img_path = os.path.join(os.path.dirname(pdf_path), 'debug_page1.png')
        pages[0].save(debug_img_path)
        print('Saved debug first page to', debug_img_path)

        # Run OCR on the first page
        print('Running pytesseract.image_to_string on the first page...')
        text = pytesseract.image_to_string(pages[0])
        print('---- OCR OUTPUT (first 1200 chars) ----')
        print(text[:1200])
        print('---- END OCR OUTPUT ----')

    except Exception as ex:
        print('EXCEPTION during run:')
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app/ocr_demo.py path\\to\\file.pdf")
    else:
        main(sys.argv[1])
