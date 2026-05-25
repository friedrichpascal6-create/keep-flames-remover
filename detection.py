"""Flame Detection Modul für Flammen-Erkennung."""

import cv2
import numpy as np
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

from config import FLAME_EMOJI_COLORS, COLOR_TOLERANCE


class FlameDetector:
    """Erkennt Flammen-Icons in Screenshots."""

    def __init__(self):
        """Initialisiert den Flame Detector."""
        self.flame_colors = FLAME_EMOJI_COLORS
        self.tolerance = COLOR_TOLERANCE

    def screenshot_to_array(self, screenshot_base64):
        """Konvertiert Base64 Screenshot zu OpenCV Array."""
        try:
            # Decode base64
            image_data = np.frombuffer(
                screenshot_base64, dtype=np.uint8
            )
            # Decode image
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            logger.error(f"Fehler bei Screenshot-Konvertierung: {e}")
            return None

    def detect_flame_color(self, image):
        """Erkennt Flammen-Farben im Bild."""
        if image is None:
            return False
        
        # Convert BGR to HSV für bessere Farberkennung
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Orange Bereich (Flammen)
        lower_orange = np.array([5, 100, 100])
        upper_orange = np.array([25, 255, 255])
        
        # Erstelle Maske für Orange
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        
        # Überprüfe, ob genug Orange-Pixel vorhanden sind
        orange_pixels = cv2.countNonZero(mask)
        
        # Wenn mehr als 100 Pixel Orange, ist eine Flamme vorhanden
        return orange_pixels > 100

    def has_flame(self, driver):
        """Überprüft, ob die aktuelle Zelle Flammen-Icon hat."""
        try:
            # Mache Screenshot
            screenshot = driver.get_screenshot_as_base64()
            
            # Konvertiere zu Array
            image = self.screenshot_to_array(
                np.frombuffer(
                    np.frombuffer(
                        bytes.fromhex(screenshot),
                        dtype=np.uint8
                    ),
                    dtype=np.uint8
                )
            )
            
            # Erkenne Flamme
            return self.detect_flame_color(image)
            
        except Exception as e:
            logger.error(f"Fehler bei Flame Detection: {e}")
            return False