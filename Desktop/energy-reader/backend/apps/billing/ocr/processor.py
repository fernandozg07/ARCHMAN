import os
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from pyzbar import pyzbar
import pytesseract
from paddleocr import PaddleOCR
from dataclasses import dataclass
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class OCRResult:
    """Result of OCR processing"""
    success: bool
    text: str = ""
    barcodes: List[dict] = None
    error: str = ""
    
    def __post_init__(self):
        if self.barcodes is None:
            self.barcodes = []


class OCRProcessor:
    """OCR processor with multiple engines and preprocessing"""
    
    def __init__(self, use_paddle=True, use_tesseract=True):
        self.use_paddle = use_paddle
        self.use_tesseract = use_tesseract
        
        # Initialize PaddleOCR
        if self.use_paddle:
            try:
                self.paddle_ocr = PaddleOCR(use_angle_cls=True, lang='pt', use_gpu=False)
            except Exception as e:
                logger.warning(f"Failed to initialize PaddleOCR: {e}")
                self.use_paddle = False
        
        # Configure Tesseract
        if self.use_tesseract:
            tesseract_cmd = os.getenv('TESSERACT_CMD', 'tesseract')
            if tesseract_cmd != 'tesseract':
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    def process_file(self, file_path: str) -> OCRResult:
        """Process file (PDF/image) with OCR"""
        try:
            # Convert PDF to images if needed
            images = self._load_images(file_path)
            
            if not images:
                return OCRResult(success=False, error="No images to process")
            
            all_text = []
            all_barcodes = []
            
            for image in images:
                # Preprocess image
                processed_image = self._preprocess_image(image)
                
                # Extract text
                text = self._extract_text(processed_image)
                if text:
                    all_text.append(text)
                
                # Extract barcodes
                barcodes = self._extract_barcodes(processed_image)
                all_barcodes.extend(barcodes)
            
            combined_text = "\n".join(all_text)
            
            return OCRResult(
                success=True,
                text=combined_text,
                barcodes=all_barcodes
            )
            
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            return OCRResult(success=False, error=str(e))
    
    def _load_images(self, file_path: str) -> List[np.ndarray]:
        """Load images from file (PDF or image)"""
        images = []
        
        try:
            if file_path.lower().endswith('.pdf'):
                # Convert PDF to images
                pil_images = convert_from_path(file_path, dpi=300)
                for pil_img in pil_images:
                    # Convert PIL to OpenCV format
                    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                    images.append(cv_img)
            else:
                # Load image directly
                image = cv2.imread(file_path)
                if image is not None:
                    images.append(image)
        
        except Exception as e:
            logger.error(f"Failed to load images from {file_path}: {e}")
        
        return images
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Deskew
            gray = self._deskew_image(gray)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Enhance contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(denoised)
            
            # Binarization
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return binary
            
        except Exception as e:
            logger.warning(f"Preprocessing failed, using original: {e}")
            return image
    
    def _deskew_image(self, image: np.ndarray) -> np.ndarray:
        """Deskew image using Hough transform"""
        try:
            edges = cv2.Canny(image, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
            
            if lines is not None:
                angles = []
                for rho, theta in lines[:10]:  # Use first 10 lines
                    angle = theta * 180 / np.pi
                    if angle < 45:
                        angles.append(angle)
                    elif angle > 135:
                        angles.append(angle - 180)
                
                if angles:
                    median_angle = np.median(angles)
                    if abs(median_angle) > 0.5:  # Only rotate if significant skew
                        (h, w) = image.shape[:2]
                        center = (w // 2, h // 2)
                        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                        return rotated
        
        except Exception as e:
            logger.warning(f"Deskewing failed: {e}")
        
        return image
    
    def _extract_text(self, image: np.ndarray) -> str:
        """Extract text using available OCR engines"""
        texts = []
        
        # Try PaddleOCR first (usually better for Portuguese)
        if self.use_paddle:
            try:
                result = self.paddle_ocr.ocr(image, cls=True)
                if result and result[0]:
                    paddle_text = "\n".join([line[1][0] for line in result[0] if line[1][1] > 0.5])
                    if paddle_text:
                        texts.append(paddle_text)
            except Exception as e:
                logger.warning(f"PaddleOCR failed: {e}")
        
        # Try Tesseract
        if self.use_tesseract:
            try:
                tesseract_text = pytesseract.image_to_string(
                    image, 
                    lang='por',
                    config='--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüý .,;:!?()[]{}/-'
                )
                if tesseract_text.strip():
                    texts.append(tesseract_text)
            except Exception as e:
                logger.warning(f"Tesseract failed: {e}")
        
        # Combine results (prefer PaddleOCR if available)
        if texts:
            return texts[0] if len(texts) == 1 else "\n".join(texts)
        
        return ""
    
    def _extract_barcodes(self, image: np.ndarray) -> List[dict]:
        """Extract barcodes and QR codes"""
        barcodes = []
        
        try:
            decoded_objects = pyzbar.decode(image)
            
            for obj in decoded_objects:
                barcode_data = {
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'rect': {
                        'x': obj.rect.left,
                        'y': obj.rect.top,
                        'width': obj.rect.width,
                        'height': obj.rect.height
                    }
                }
                barcodes.append(barcode_data)
                
        except Exception as e:
            logger.warning(f"Barcode extraction failed: {e}")
        
        return barcodes