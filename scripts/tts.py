#!/usr/bin/env python3
"""
Text-to-Speech Module for Reading Eye - Raspberry Pi Version
- Uses pyttsx3 for offline TTS (primary)
- Falls back to gTTS for better language support
- Supports multiple languages: Arabic, French, English
- Optimized for headless Raspberry Pi operation
"""
import pyttsx3
import threading
import queue
import time
import os
import logging
from gtts import gTTS
import tempfile
import subprocess

logger = logging.getLogger(__name__)

class TTS:
    """Text-to-Speech engine using pyttsx3 and gTTS"""
    
    def __init__(self, language='fr', rate=150, volume=0.9, use_gtts=False):
        """
        Initialize TTS engine
        
        Args:
            language: Language code (fr, en, ar)
            rate: Speech rate (words per minute)
            volume: Volume level (0.0-1.0)
            use_gtts: Use gTTS instead of pyttsx3 (for better Arabic support)
        """
        self.language = language
        self.rate = rate
        self.volume = volume
        self.use_gtts = use_gtts
        self.engine = None
        
        self._queue = queue.Queue()
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            daemon=True
        )
        self._stop_event = threading.Event()
        
        self._init_engine()
        self._worker_thread.start()
        
        self.temp_files = []  # For cleanup
        logger.info(f"TTS initialized: language={language}, rate={rate}, volume={volume}")

    def _init_engine(self):
        """Initialize the TTS engine"""
        try:
            if self.use_gtts:
                logger.info("Using gTTS for TTS")
                return
            
            self.engine = pyttsx3.init()
            
            # Configure rate and volume
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Try to set voice based on language
            voices = self.engine.getProperty('voices')
            logger.info(f"Available voices: {[v.name for v in voices]}")
            
            logger.info(f"pyttsx3 TTS initialized - Language: {self.language}")
        except Exception as e:
            logger.error(f"TTS engine initialization error: {e}")
            self.engine = None

    def set_language(self, language):
        """Change TTS language"""
        self.language = language
        logger.info(f"TTS language changed to: {language}")

    def set_rate(self, rate):
        """Change speech rate"""
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)
        logger.info(f"TTS rate changed to: {rate}")

    def set_volume(self, volume):
        """Change volume"""
        self.volume = volume
        if self.engine:
            self.engine.setProperty('volume', volume)
        logger.info(f"TTS volume changed to: {volume}")

    def speak(self, text):
        """Queue text for speech"""
        if not text or not text.strip():
            return
        
        # Add to queue for background worker
        self._queue.put(text.strip())
        logger.debug(f"Queued for TTS: {text[:100]}")

    def _worker_loop(self):
        """Background worker for TTS processing"""
        while not self._stop_event.is_set():
            try:
                # Wait for text with timeout to allow checking stop event
                text = self._queue.get(timeout=1.0)
                if text:
                    self._speak_text(text)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"TTS worker error: {e}")

    def _speak_text(self, text):
        """Actually speak the text"""
        try:
            if self.use_gtts:
                self._speak_gtts(text)
            else:
                self._speak_pyttsx3(text)
        except Exception as e:
            logger.error(f"Error speaking text: {e}")

    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3"""
        if not self.engine:
            logger.warning("pyttsx3 engine not available")
            return
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            logger.info(f"Spoke {len(text)} chars via pyttsx3")
        except Exception as e:
            logger.error(f"pyttsx3 speech error: {e}")

    def _speak_gtts(self, text):
        """Speak using Google Text-to-Speech"""
        try:
            # Map language codes
            lang_map = {'fr': 'fr', 'en': 'en', 'ar': 'ar'}
            lang = lang_map.get(self.language[:2], 'fr')
            
            # Generate speech
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_file = f.name
                tts.save(temp_file)
            
            self.temp_files.append(temp_file)
            
            # Play using system tools
            self._play_audio(temp_file)
            
            logger.info(f"Spoke {len(text)} chars via gTTS")
        except Exception as e:
            logger.error(f"gTTS error: {e}")

    @staticmethod
    def _play_audio(file_path):
        """Play audio file using available system tools"""
        try:
            # Try different audio players
            players = [
                ['mpg123', file_path],
                ['play', file_path],  # SoX
                ['ffplay', '-nodisp', '-autoexit', file_path],
                ['cvlc', '--play-and-exit', file_path],
            ]
            
            for player_cmd in players:
                try:
                    subprocess.run(
                        player_cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=60
                    )
                    return
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    continue
            
            logger.warning("No audio player found")
        except Exception as e:
            logger.error(f"Audio playback error: {e}")

    def stop(self):
        """Stop TTS and cleanup"""
        self._stop_event.set()
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        
        # Cleanup temp files
        for f in self.temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass
        
        logger.info("TTS stopped and cleaned up")

    def wait_for_completion(self, timeout=10):
        """Wait for all queued speech to complete"""
        start = time.time()
        while not self._queue.empty() and (time.time() - start) < timeout:
            time.sleep(0.1)
