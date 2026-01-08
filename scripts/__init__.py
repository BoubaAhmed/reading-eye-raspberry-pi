"""
Reading Eye - Raspberry Pi Package
OCR and Text-to-Speech for accessibility
"""

__version__ = '1.0.0'
__author__ = 'Reading Eye Project'

from .camera import PiCamera
from .ocr import OCR
from .tts import TTS

__all__ = ['PiCamera', 'OCR', 'TTS']
