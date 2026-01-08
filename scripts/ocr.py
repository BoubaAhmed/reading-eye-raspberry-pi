#!/usr/bin/env python3
"""
OCR Module for Reading Eye - Raspberry Pi Version
- Uses Tesseract for text extraction
- Supports multiple languages: Arabic, French, English
- Optimized for Raspberry Pi with headless operation
"""
import os
import pytesseract
import shutil
import subprocess
import re
import logging

logger = logging.getLogger(__name__)

class OCR:
    """Tesseract-based OCR for Reading Eye"""
    
    def __init__(self, tesseract_cmd=None, tessdata_prefix=None):
        """
        Initialize OCR engine
        
        Args:
            tesseract_cmd: Path to tesseract binary (auto-detected if None)
            tessdata_prefix: Path to tessdata directory (auto-detected if None)
        """
        # Priority: explicit arg > env var > which > fallback
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            pytesseract.pytesseract.tesseract_cmd = (
                os.environ.get('TESSERACT_CMD') or
                shutil.which('tesseract') or
                '/usr/bin/tesseract'  # Common path on Linux/Pi
            )

        if tessdata_prefix:
            os.environ['TESSDATA_PREFIX'] = tessdata_prefix
        elif 'TESSDATA_PREFIX' not in os.environ:
            # Try to auto-detect tessdata on Pi
            possible_paths = [
                '/usr/share/tesseract-ocr',
                '/usr/share/tesseract',
                '/opt/tesseract/share'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    os.environ['TESSDATA_PREFIX'] = path
                    break

        self.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd
        self.tessdata_prefix = os.environ.get('TESSDATA_PREFIX', '')
        
        logger.info(f"OCR initialized with tesseract: {self.tesseract_cmd}")
        logger.info(f"TESSDATA_PREFIX: {self.tessdata_prefix}")

    def set_tesseract_cmd(self, path):
        """Set tesseract executable path"""
        if path and os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            self.tesseract_cmd = path
            logger.info(f"Tesseract path set to: {path}")

    def set_tessdata_prefix(self, path):
        """Set tessdata directory path"""
        if path and os.path.exists(path):
            os.environ['TESSDATA_PREFIX'] = path
            self.tessdata_prefix = path
            logger.info(f"TESSDATA_PREFIX set to: {path}")

    def is_available(self):
        """Check if tesseract is available and working"""
        cmd = self.tesseract_cmd
        try:
            res = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=3
            )
            out = (res.stdout or '') + (res.stderr or '')
            is_ok = res.returncode == 0 and ('tesseract' in out.lower() or 'version' in out.lower())
            if is_ok:
                logger.info("✓ Tesseract is available")
            else:
                logger.warning("✗ Tesseract version check failed")
            return is_ok
        except Exception as e:
            logger.error(f"Tesseract check error: {e}")
            return False

    def get_installed_languages(self):
        """Get list of installed tesseract languages"""
        cmd = self.tesseract_cmd
        try:
            res = subprocess.run(
                [cmd, '--list-langs'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if res.returncode == 0:
                lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
                # Filter out header lines, keep only language codes
                langs = [l for l in lines if all(c.isalpha() or c == '-' for c in l)]
                logger.info(f"Available languages: {langs}")
                return langs
        except Exception as e:
            logger.error(f"Error listing languages: {e}")
        return []

    def extract_text_from_image(self, image, lang='eng'):
        """
        Extract text from an image using OCR
        
        Args:
            image: OpenCV image (grayscale or color)
            lang: Language code (eng, fra, ara, or combinations like 'eng+fra')
        
        Returns:
            Extracted text string
        """
        try:
            # Map 2-letter codes to 3-letter tesseract codes
            language = self._map_language_code(lang)

            # Configure tesseract based on language
            config = '--oem 3 --psm 6'
            if 'ara' in language.lower():
                # Arabic: preserve interword spaces
                config = '--oem 3 --psm 6 -c preserve_interword_spaces=1'

            # Run OCR
            text = pytesseract.image_to_string(image, lang=language, config=config)
            
            # Clean text based on language
            text = self._clean_text(text, language)
            
            return text.strip()
        except FileNotFoundError as e:
            logger.error(f"OCR file error: {e}")
            return ""
        except Exception as e:
            logger.error(f"OCR extraction error: {e}")
            return ""

    @staticmethod
    def _map_language_code(lang):
        """Map 2-letter codes to 3-letter tesseract codes"""
        mapping = {
            'en': 'eng',
            'fr': 'fra',
            'ar': 'ara',
            'es': 'spa',
            'de': 'deu',
            'it': 'ita',
            'pt': 'por',
            'ru': 'rus',
        }
        
        # Handle compound languages (e.g., 'eng+fra')
        if '+' in lang:
            parts = [mapping.get(p[:2], p) for p in lang.split('+')]
            return '+'.join(parts)
        
        return mapping.get(lang[:2], lang)

    @staticmethod
    def _clean_text(text, language):
        """Clean OCR output based on language"""
        if not text:
            return ""
        
        if 'ara' in language.lower():
            # Keep Arabic characters and punctuation
            text = re.sub(r"[^\u0600-\u06FF\s.,?!;:'\"()\-]", "", text)
        else:
            # Keep Latin characters and punctuation
            text = re.sub(r"[^a-zA-Z0-9À-ÿ.,?!;:'\"()\-\s]", "", text)
        
        # Normalize multiple spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text
