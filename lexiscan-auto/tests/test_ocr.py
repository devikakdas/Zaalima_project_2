import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import pytest
from src.data.ocr_processor import OCRProcessor
from pathlib import Path


def test_ocr_initialization():
    """Test that OCR processor initializes correctly"""
    processor = OCRProcessor()
    assert processor.min_confidence == 60.0
    assert processor.dpi == 300


def test_preprocess_image():
    """Test image preprocessing"""
    from PIL import Image
    import numpy as np

    # Create a simple test image
    img_array = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    image = Image.fromarray(img_array)

    processor = OCRProcessor()
    processed = processor.preprocess_image(image)

    assert processed.mode == 'L'  # Grayscale
    assert processed.size == (100, 100)

# To run tests:
# pytest tests/test_ocr.py -v
