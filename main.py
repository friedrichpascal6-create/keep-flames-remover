#!/usr/bin/env python3
"""Keep Flames Remover - Hauptskript

Entfernt automatisch Snapchat-Freunde ohne aktive Flammen (Streaks).
"""

import time
import logging
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import (
    APPIUM_HOST,
    APPIUM_PORT,
    SNAPCHAT_BUNDLE_ID,
    DELAY_BETWEEN_TAPS,
    WAIT_FOR_ELEMENT,
    DEBUG_MODE,
    LOG_FILE,
)
from detection import FlameDetector
from utils import setup_logging, load_protected_friends

# Logging Setup
logger = setup_logging(LOG_FILE, DEBUG_MODE)


class SnapchatFlameRemover:
    """Entfernt Snapchat-Freunde ohne Flammen."""

    def __init__(self):
        """Initialisiert den Remover."""
        self.driver = None
        self.flame_detector = FlameDetector()
        self.protected_friends = load_protected_friends()
        self.removed_count = 0
        self.skipped_count = 0

    def connect_to_device(self):
        """Verbindet sich mit dem iOS Simulator/Gerät."""
        logger.info("Verbinde mit iOS Gerät...")
        
        options = XCUITestOptions()
        options.bundle_id = SNAPCHAT_BUNDLE_ID
        options.platform_name = "iOS"
        options.automation_name = "XCUITest"
        
        try:
            self.driver = webdriver.Remote(
                f"http://{APPIUM_HOST}:{APPIUM_PORT}",
                options=options
            )
            logger.info("✓ Erfolgreich mit Snapchat verbunden")
            return True
        except Exception as e:
            logger.error(f"✗ Fehler beim Verbinden: {e}")
            logger.error("Stelle sicher, dass Appium läuft: appium --relaxed-security")
            return False

    def open_friends_list(self):
        """Öffnet die Snapchat Freundesliste."""
        logger.info("Öffne Freundesliste...")
        
        try:
            # Swipe nach links um zum Friends Tab zu gelangen
            self.driver.swipe(start_x=200, start_y=400, end_x=50, end_y=400, duration=500)
            time.sleep(1)
            logger.info("✓ Freundesliste geöffnet")
            return True
        except Exception as e:
            logger.error(f"✗ Fehler beim Öffnen der Freundesliste: {e}")
            return False

    def get_friends(self):
        """Holt die Liste aller Freunde."""
        logger.info("Lade Freundesliste...")
        
        try:
            # Versuche alle Friend-Zellen zu finden
            friends = self.driver.find_elements(
                AppiumBy.XPATH,
                "//XCUIElementTypeCell[contains(@name, 'friend')]"
            )
            logger.info(f"✓ {len(friends)} Freunde gefunden")
            return friends
        except Exception as e:
            logger.error(f"✗ Fehler beim Laden der Freundesliste: {e}")
            return []

    def check_for_flames(self, friend_element):
        """Überprüft, ob ein Freund Flammen-Icon hat."""
        try:
            # Suche nach Flammen-Emoji oder -Icon in der Zelle
            flame_indicator = friend_element.find_element(
                AppiumBy.XPATH,
                ".//XCUIElementTypeImage[contains(@name, 'flame')]"
            )
            return True
        except NoSuchElementException:
            return False

    def remove_friend(self, friend_name):
        """Entfernt einen Freund."""
        logger.info(f"Entferne Freund: {friend_name}")
        
        try:
            # Long Press auf Freund
            friend_cell = self.driver.find_element(
                AppiumBy.XPATH,
                f"//XCUIElementTypeCell[contains(@name, '{friend_name}')]"
            )
            
            # Perform long press
            self.driver.execute_script(
                "mobile: touchAndHold",
                {"element": friend_cell, "duration": 1}
            )
            time.sleep(0.5)
            
            # Tippe auf "Remove" Button
            remove_button = WebDriverWait(self.driver, WAIT_FOR_ELEMENT).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@label, 'Remove')]")
                )
            )
            remove_button.click()
            
            # Bestätige Entfernung
            confirm_button = WebDriverWait(self.driver, WAIT_FOR_ELEMENT).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@label, 'Confirm')]")
                )
            )
            confirm_button.click()
            
            logger.info(f"✓ {friend_name} erfolgreich entfernt")
            self.removed_count += 1
            time.sleep(DELAY_BETWEEN_TAPS)  # Verzögerung zwischen Entfernungen
            return True
            
        except TimeoutException:
            logger.error(f"✗ Timeout beim Entfernen von {friend_name}")
            return False
        except Exception as e:
            logger.error(f"✗ Fehler beim Entfernen von {friend_name}: {e}")
            return False

    def run(self):
        """Führt den Haupt-Prozess aus."""
        logger.info("="*50)
        logger.info("Keep Flames Remover - START")
        logger.info("="*50)
        
        # Mit Gerät verbinden
        if not self.connect_to_device():
            return
        
        # Freundesliste öffnen
        if not self.open_friends_list():
            self.driver.quit()
            return
        
        time.sleep(1)
        
        # Freunde durchgehen
        friends = self.get_friends()
        
        if not friends:
            logger.warning("Keine Freunde gefunden")
            self.driver.quit()
            return
        
        for friend in friends:
            try:
                friend_name = friend.get_attribute("name")
                
                # Überspringe geschützte Freunde
                if friend_name in self.protected_friends:
                    logger.info(f"⭐ {friend_name} ist geschützt - überspringe")
                    self.skipped_count += 1
                    continue
                
                # Überprüfe auf Flammen
                if self.check_for_flames(friend):
                    logger.info(f"🔥 {friend_name} hat Flammen - behalte")
                    self.skipped_count += 1
                else:
                    # Entferne Freund ohne Flammen
                    self.remove_friend(friend_name)
                    
            except Exception as e:
                logger.error(f"✗ Fehler bei Freund: {e}")
                continue
        
        # Zusammenfassung
        logger.info("="*50)
        logger.info("ZUSAMMENFASSUNG")
        logger.info(f"Entfernte Freunde: {self.removed_count}")
        logger.info(f"Behaltene Freunde: {self.skipped_count}")
        logger.info(f"Gesamt: {self.removed_count + self.skipped_count}")
        logger.info("="*50)
        logger.info("✓ Prozess abgeschlossen")
        
        # Cleanup
        self.driver.quit()


if __name__ == "__main__":
    remover = SnapchatFlameRemover()
    remover.run()