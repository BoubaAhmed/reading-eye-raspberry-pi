#!/usr/bin/env python3
"""
Reading Eye - Main Application for Raspberry Pi
- Runs over SSH without GUI
- Captures images with Pi Camera
- Performs OCR and text-to-speech
- Supports single capture and continuous loop modes
"""
import argparse
import logging
import sys
import os
import json
import time
from pathlib import Path

# Import local modules
from camera import PiCamera
from ocr import OCR
from tts import TTS

# Setup logging
LOG_DIR = Path(__file__).parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'reading_eye.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ReadingEyeApp:
    """Main Reading Eye application"""
    
    def __init__(self, config_path=None):
        """
        Initialize application
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        
        # Initialize components
        self.camera = PiCamera(resolution=self.config.get('camera_resolution', (1280, 720)))
        self.ocr = OCR(
            tesseract_cmd=self.config.get('tesseract_path'),
            tessdata_prefix=self.config.get('tessdata_prefix')
        )
        self.tts = TTS(
            language=self.config.get('tts_language', 'fr'),
            rate=self.config.get('tts_rate', 150),
            volume=self.config.get('tts_volume', 0.9)
        )
        
        logger.info("Reading Eye App initialized")

    def _get_default_config_path(self):
        """Get default config file path"""
        base_dir = Path(__file__).parent.parent
        return base_dir / 'config' / 'reading_eye_config.json'

    def _load_config(self):
        """Load configuration file"""
        default_config = {
            'ocr_language': 'fra+eng',
            'tts_language': 'fr',
            'camera_resolution': [1920, 1080],
            'tts_rate': 150,
            'tts_volume': 0.9,
            'tesseract_path': '/usr/bin/tesseract',
            'tessdata_prefix': '/usr/share/tesseract-ocr'
        }
        
        try:
            if self.config_path and os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
                    logger.info(f"Config loaded from: {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        
        return default_config

    def capture_single(self, lang=None, save_image=False):
        """
        Capture single frame and process
        
        Args:
            lang: OCR language (default from config)
            save_image: Save captured image to disk
        """
        lang = lang or self.config.get('ocr_language', 'fra+eng')
        
        logger.info("Capturing single frame...")
        
        # Capture
        gray = self.camera.get_grayscale_frame()
        if gray is None:
            logger.error("Failed to capture frame")
            return False
        
        # Save if requested
        if save_image:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            capture_dir = Path(__file__).parent.parent / 'capture'
            capture_dir.mkdir(exist_ok=True)
            image_path = capture_dir / f'capture_{timestamp}.png'
            self.camera.capture_with_save(str(image_path))
        
        # OCR
        logger.info(f"Running OCR with language: {lang}")
        text = self.ocr.extract_text_from_image(gray, lang=lang)
        
        if text:
            logger.info("=== Detected Text ===")
            print(text)
            logger.info("====================")
            
            # TTS
            logger.info("Speaking text...")
            self.tts.speak(text)
            self.tts.wait_for_completion(timeout=20)
        else:
            logger.warning("No text detected in image")
        
        return True

    def capture_loop(self, interval=5.0, lang=None, duration=None):
        """
        Continuous capture loop
        
        Args:
            interval: Seconds between captures
            lang: OCR language (default from config)
            duration: Total duration in seconds (None = infinite)
        """
        lang = lang or self.config.get('ocr_language', 'fra+eng')
        start_time = time.time()
        last_text = ""
        
        logger.info(f"Starting capture loop: interval={interval}s, duration={duration}s")
        
        try:
            while True:
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    logger.info("Duration reached, stopping")
                    break
                
                # Capture and process
                gray = self.camera.get_grayscale_frame()
                if gray is None:
                    logger.error("Capture failed, skipping")
                    time.sleep(interval)
                    continue
                
                # OCR
                text = self.ocr.extract_text_from_image(gray, lang=lang)
                
                # Only speak if text changed
                if text and text != last_text:
                    logger.info(f"New text detected: {text[:100]}")
                    self.tts.speak(text)
                    last_text = text
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("Capture loop interrupted by user")
        
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up...")
        if self.camera:
            self.camera.close()
        if self.tts:
            self.tts.stop()
        logger.info("Cleanup complete")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Reading Eye - Raspberry Pi OCR + TTS Application'
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--single',
        action='store_true',
        help='Capture single frame and process'
    )
    mode_group.add_argument(
        '--loop',
        action='store_true',
        help='Continuous capture loop'
    )
    
    # Options
    parser.add_argument(
        '--interval',
        type=float,
        default=5.0,
        help='Capture interval in seconds (for loop mode, default: 5.0)'
    )
    parser.add_argument(
        '--duration',
        type=float,
        help='Duration in seconds (for loop mode, default: infinite)'
    )
    parser.add_argument(
        '--lang',
        default='fra+eng',
        help='OCR language (eng, fra, ara, or combinations like eng+fra)'
    )
    parser.add_argument(
        '--save-image',
        action='store_true',
        help='Save captured images to disk'
    )
    parser.add_argument(
        '--config',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize app
        app = ReadingEyeApp(config_path=args.config)
        
        # Run
        if args.single:
            app.capture_single(lang=args.lang, save_image=args.save_image)
        elif args.loop:
            app.capture_loop(
                interval=args.interval,
                lang=args.lang,
                duration=args.duration
            )
    
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
