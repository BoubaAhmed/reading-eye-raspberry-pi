#!/usr/bin/env python3
"""
Camera Module for Reading Eye - Raspberry Pi
- Handles Pi Camera 3/5 using Picamera2
- Supports single capture and continuous streaming
"""
import cv2
import time
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False
    logger.warning("Picamera2 not available - using fallback mode")


class PiCamera:
    """Raspberry Pi Camera handler using Picamera2"""
    
    def __init__(self, resolution=(1280, 720)):
        """
        Initialize camera
        
        Args:
            resolution: Tuple (width, height) for capture
        """
        self.resolution = resolution
        self.camera = None
        self.initialized = False
        
        if PICAMERA2_AVAILABLE:
            self._init_camera()
        else:
            logger.warning("Picamera2 not available")

    def _init_camera(self):
        """Initialize Picamera2"""
        try:
            self.camera = Picamera2()
            config = self.camera.create_still_configuration(
                main={"size": self.resolution}
            )
            self.camera.configure(config)
            self.camera.start()
            
            # Warmup
            time.sleep(1.0)
            
            self.initialized = True
            logger.info(f"Camera initialized: {self.resolution}")
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            self.initialized = False

    def capture_frame(self):
        """
        Capture a single frame
        
        Returns:
            OpenCV image (BGR) or None if failed
        """
        if not self.initialized or not self.camera:
            logger.error("Camera not initialized")
            return None
        
        try:
            # Capture RGB array from Picamera2
            arr = self.camera.capture_array()
            
            # Convert RGB to BGR for OpenCV
            frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            
            logger.debug(f"Frame captured: {frame.shape}")
            return frame
        except Exception as e:
            logger.error(f"Capture error: {e}")
            return None

    def capture_with_save(self, output_path):
        """
        Capture frame and save to file
        
        Args:
            output_path: Path to save the image
        
        Returns:
            True if successful
        """
        frame = self.capture_frame()
        if frame is None:
            return False
        
        try:
            cv2.imwrite(output_path, frame)
            logger.info(f"Frame saved to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Save error: {e}")
            return False

    def get_grayscale_frame(self):
        """
        Capture and convert to grayscale for OCR
        
        Returns:
            Grayscale OpenCV image or None
        """
        frame = self.capture_frame()
        if frame is None:
            return None
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return gray
        except Exception as e:
            logger.error(f"Grayscale conversion error: {e}")
            return None

    def close(self):
        """Close camera and release resources"""
        if self.camera:
            try:
                self.camera.stop()
                logger.info("Camera closed")
            except Exception as e:
                logger.error(f"Camera close error: {e}")

    def __enter__(self):
        """Context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.close()
