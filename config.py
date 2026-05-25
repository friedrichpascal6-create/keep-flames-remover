"""Konfiguration für Keep Flames Remover"""

# Appium Server Konfiguration
APPIUM_HOST = "127.0.0.1"
APPIUM_PORT = 4723

# Snapchat App Konfiguration
SNAPCHAT_APP_ID = "com.toyopagroup.picaboo"
SNAPCHAT_BUNDLE_ID = "com.toyopagroup.picaboo"

# Timing Konfiguration
DELAY_BETWEEN_TAPS = 2.5  # Sekunden zwischen Entfernungen (2-3 Sekunden)
WAIT_FOR_ELEMENT = 5  # Sekunden warten auf Element
DELAY_AFTER_TAP = 1.0  # Kurze Verzögerung nach jedem Tap

# Screen Koordinaten (für iPhone 12 Simulator - anpassen wenn nötig)
FRIENDS_LIST_BUTTON = (50, 100)  # Freundesliste öffnen
SCREEN_CENTER_X = 190
SCREEN_CENTER_Y = 400

# Flammen-Erkennung
FLAME_EMOJI_COLORS = [
    (255, 100, 0),  # Orange
    (255, 165, 0),  # Orange-Gelb
]
COLOR_TOLERANCE = 50  # Farbtoleranz für Erkennung

# Logging
DEBUG_MODE = True
LOG_FILE = "flame_remover.log"

# Protected Friends (werden nicht gelöscht)
PROTECTED_FRIENDS_FILE = "protected_friends.txt"