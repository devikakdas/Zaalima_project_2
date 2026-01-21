import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from src.data.ocr_processor import OCRProcessor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)


def main():
    # print("test")
    # Initialize processor
    processor = OCRProcessor()

    # Process the sample contract
    result = processor.process_document("../data/raw/sample_contract.pdf")

    if result['success']:
        print("\n" + "=" * 60)
        print("✓ OCR EXTRACTION SUCCESSFUL")
        print("=" * 60)
        print(f"Total pages: {result['total_pages']}")

        for page_data in result['pages']:
            print(f"\n--- Page {page_data['page']} ---")
            print(f"Method: {page_data['method']}")
            print(f"Confidence: {page_data['confidence']}%")
            print(f"\nExtracted Text:")
            print(page_data['text'][:500])  # First 500 chars
    else:
        print(f"✗ Error: {result['error']}")


if __name__ == "__main__":
    main()


# from pathlib import Path
#
# from src.data.ocr_processor import OCRProcessor
# import logging
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#
# # Setup logging
# logging.basicConfig(level=logging.INFO)
#
#
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# def test_ocr_initialization():
#     pdf_path = PROJECT_ROOT / "data" / "raw" / "sample_contract.pdf"
#     assert pdf_path.exists()
#     # Initialize processor
#     processor = OCRProcessor()
#
#     # Process the sample contract
#     result = processor.process_document(str(pdf_path))
#
#     if result['success']:
#         print("\n" + "=" * 60)
#         print("✓ OCR EXTRACTION SUCCESSFUL")
#         print("=" * 60)
#         print(f"Total pages: {result['total_pages']}")
#
#         for page_data in result['pages']:
#             print(f"\n--- Page {page_data['page']} ---")
#             print(f"Method: {page_data['method']}")
#             print(f"Confidence: {page_data['confidence']}%")
#             print(f"\nExtracted Text:")
#             print(page_data['text'][:500])  # First 500 chars
#     else:
#         print(f"✗ Error: {result['error']}")
#
#
