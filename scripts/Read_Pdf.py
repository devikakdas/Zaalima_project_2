def Read_Pdf(Input_path):
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    from ocr_processor import OCRProcessor
    import logging

    # Setup logging
    logging.basicConfig(level=logging.INFO)

    processor = OCRProcessor()

    # Process the sample contract
    result = processor.process_document(Input_path)
    
    output = result["pages"][0]['text']
    
    return output




