import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from pdf2image import convert_from_path
import pdfplumber
from typing import Dict, List, Optional
import logging
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class OCRProcessor:
    """
    Extracts text from PDF contracts.
    Handles both digital PDFs and scanned documents.
    """

    def __init__(self, min_confidence: float = 60.0, dpi: int = 300):
        """
        Initialize OCR processor

        Args:
            min_confidence: Minimum quality score (0-100) to accept OCR results
            dpi: Image resolution (higher = better quality but slower)
        """
        self.min_confidence = min_confidence
        self.dpi = dpi

        # Verify Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
            logger.info("✓ Tesseract OCR is ready")
        except Exception as e:
            raise RuntimeError(
                "Tesseract not installed. Run: sudo apt install tesseract-ocr"
            )

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Clean up image for better OCR accuracy.

        Steps:
        1. Convert to grayscale (removes color, reduces noise)
        2. Increase contrast (makes text darker, background lighter)
        3. Sharpen edges (makes letters clearer)
        4. Remove noise (smooth out scan artifacts)
        5. Binarize (pure black text on white background)
        """
        # Grayscale conversion
        image = image.convert('L')

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)

        # Sharpen
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.5)

        # Remove noise
        image = image.filter(ImageFilter.MedianFilter(size=3))

        # Binarization (black & white only)
        img_array = np.array(image)
        threshold = np.mean(img_array)
        binary = (img_array > threshold) * 255
        image = Image.fromarray(binary.astype(np.uint8))

        return image

    def extract_text_native(self, pdf_path: str) -> Dict:
        """
        Fast extraction from digital PDFs (PDFs created on computer).
        Works when PDF already contains text.
        """
        try:
            text_pages = []

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()

                    if text and text.strip():
                        text_pages.append({
                            'page': page_num,
                            'text': text,
                            'method': 'native',
                            'confidence': 100.0
                        })

            return {
                'success': True,
                'pages': text_pages,
                'total_pages': len(text_pages)
            }
        except Exception as e:
            logger.error(f"Native extraction failed: {e}")
            return {'success': False, 'error': str(e)}

    def extract_text_ocr(self, pdf_path: str) -> Dict:
        """
        Slower extraction from scanned PDFs (photos/scans of paper).
        Uses OCR to "read" the image.
        """
        try:
            # Convert PDF pages to images
            logger.info(f"Converting PDF to images at {self.dpi} DPI...")
            images = convert_from_path(pdf_path, dpi=self.dpi)

            text_pages = []

            for page_num, image in enumerate(images, 1):
                logger.info(f"Processing page {page_num}/{len(images)}...")

                # Clean up image
                clean_image = self.preprocess_image(image)

                # Get OCR confidence scores
                ocr_data = pytesseract.image_to_data(
                    clean_image,
                    output_type=pytesseract.Output.DICT
                )

                # Calculate average confidence
                confidences = [
                    int(c) for c in ocr_data['conf']
                    if c != '-1' and int(c) > 0
                ]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0

                # Extract text
                text = pytesseract.image_to_string(clean_image)

                if text.strip():
                    text_pages.append({
                        'page': page_num,
                        'text': text,
                        'method': 'ocr',
                        'confidence': round(avg_confidence, 2)
                    })

                    if avg_confidence < self.min_confidence:
                        logger.warning(
                            f"⚠ Page {page_num}: Low quality ({avg_confidence:.1f}%)"
                        )

            return {
                'success': True,
                'pages': text_pages,
                'total_pages': len(images)
            }
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {'success': False, 'error': str(e)}

    def process_document(self, pdf_path: str) -> Dict:
        """
        Smart extraction: tries fast method first, falls back to OCR.

        Process:
        1. Try native extraction (fast)
        2. If successful and has enough text → done!
        3. Otherwise, use OCR (slower but works on scans)
        """
        logger.info(f"📄 Processing: {pdf_path}")

        if not Path(pdf_path).exists():
            return {'success': False, 'error': 'File not found'}

        # Try native first
        result = self.extract_text_native(pdf_path)

        if result['success'] and result['total_pages'] > 0:
            # Check if we got meaningful text
            total_words = sum(len(p['text'].split()) for p in result['pages'])
            avg_words = total_words / result['total_pages']

            if avg_words > 50:  # At least 50 words per page
                logger.info("✓ Native extraction successful")
                return result

        # Fall back to OCR
        logger.info("→ Using OCR (scanned document)")
        return self.extract_text_ocr(pdf_path)

