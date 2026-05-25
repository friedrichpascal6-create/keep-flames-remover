"""Utility-Funktionen für Keep Flames Remover."""

import logging
import os
from pathlib import Path


def setup_logging(log_file, debug_mode=False):
    """Richtet Logging ein."""
    log_level = logging.DEBUG if debug_mode else logging.INFO
    
    # Logging Format
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def load_protected_friends(filepath="protected_friends.txt"):
    """Lädt geschützte Freunde aus Datei."""
    protected = set()
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    friend = line.strip()
                    if friend and not friend.startswith('#'):
                        protected.add(friend)
            logging.info(f"✓ {len(protected)} geschützte Freunde geladen")
        except Exception as e:
            logging.error(f"✗ Fehler beim Laden von protected_friends.txt: {e}")
    else:
        # Erstelle Beispiel-Datei
        create_protected_friends_template(filepath)
        logging.info(f"✓ protected_friends.txt erstellt (bitte bearbeiten)")
    
    return protected


def create_protected_friends_template(filepath="protected_friends.txt"):
    """Erstellt eine Beispiel protected_friends.txt Datei."""
    template = """# Hier deine Freunde eintragen, die NICHT gelöscht werden sollen
# Eine pro Zeile
# Beispiel:
# BestFriend1
# BestFriend2
# MyMom
"""
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        logging.error(f"✗ Fehler beim Erstellen von protected_friends.txt: {e}")


def validate_appium_connection(host="127.0.0.1", port=4723):
    """Überprüft, ob Appium läuft."""
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    
    if result == 0:
        logging.info(f"✓ Appium läuft auf {host}:{port}")
        return True
    else:
        logging.error(f"✗ Appium nicht erreichbar auf {host}:{port}")
        logging.error("Starte Appium mit: appium --relaxed-security")
        return False


def format_friend_name(name):
    """Formatiert einen Freundesnamen."""
    return name.strip().lower()


def write_log_summary(removed_count, skipped_count, log_file="summary.txt"):
    """Schreibt eine Zusammenfassung der Session."""
    summary = f"""Keep Flames Remover - Session Zusammenfassung
{'='*50}
Entfernte Freunde: {removed_count}
Behaltene Freunde: {skipped_count}
Gesamt: {removed_count + skipped_count}
{'='*50}
"""
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(summary + "\n")
    except Exception as e:
        logging.error(f"✗ Fehler beim Schreiben der Summary: {e}")