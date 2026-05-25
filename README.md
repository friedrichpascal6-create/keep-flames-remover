# Keep Flames Remover

Ein automatisiertes Tool zur Verwaltung deiner Snapchat-Freundesliste. Das Tool entfernt automatisch alle Freunde, mit denen du **keine aktiven Flammen (Streaks)** hast.

## Features

✅ Automatische Erkennung von Flammen-Icons  
✅ Entfernt nur Freunde ohne aktive Streaks  
✅ 2-3 Sekunden Verzögerung zwischen Entfernungen  
✅ Einmaliger Durchlauf durch die Freundesliste  
✅ Unterstützung für iOS Simulator und echte Geräte  
✅ Python + Appium basiert  

## Installation

### Voraussetzungen

- **macOS** (für iOS Development)
- **Xcode** installiert
- **Python 3.8+**
- **Node.js** (für Appium)

### Setup-Schritte

1. **Repository klonen:**
```bash
git clone https://github.com/friedrichpascal6-create/keep-flames-remover.git
cd keep-flames-remover
```

2. **Dependencies installieren:**
```bash
pip install -r requirements.txt
```

3. **Appium installieren:**
```bash
npm install -g appium
npm install -g appium-doctor
```

4. **Appium Doctor überprüfen:**
```bash
appium-doctor --ios
```

5. **iOS Simulator starten:**
```bash
open -a Simulator
```

## Verwendung

### 1. Snapchat im Simulator/Gerät öffnen
```bash
python main.py
```

### 2. Konfiguration anpassen (optional)

Bearbeite `config.py`:
```python
DELAY_BETWEEN_TAPS = 2.5  # Sekunden zwischen Entfernungen
SNAPCHAT_APP_ID = "com.toyopagroup.picaboo"
```

### 3. Freunde schützen (optional)

Füge Freundesnamen hinzu, die nicht entfernt werden sollen in `protected_friends.txt`:
```
BestFriend1
BestFriend2
```

## Wie es funktioniert

1. Verbindet sich mit Snapchat über Appium
2. Öffnet die Freundesliste
3. Scannt jeden Freund auf Flammen-Icon
4. Entfernt Freunde ohne Flammen
5. Wartet 2-3 Sekunden vor der nächsten Entfernung
6. Beendet nach einmaligem Durchlauf

## ⚠️ Wichtige Hinweise

- **Nutzerrichtlinien**: Dieses Tool verstößt potenziell gegen Snapchats ToS
- **Account-Risiko**: Dein Account könnte gesperrt werden
- **Nur für Tests**: Nutze es nur in einer Test-Umgebung!
- **Verzögerungen**: Die 2-3 Sekunden Verzögerung reduzieren das Block-Risiko

## Troubleshooting

### Appium verbindet sich nicht
```bash
appium --relaxed-security
```

### Snapchat wird nicht erkannt
- Stelle sicher, dass Snapchat im Simulator installiert ist
- Überprüfe die App-ID in `config.py`

### Flammen werden nicht erkannt
- Passe die Bildschirm-Koordinaten in `detection.py` an
- Überprüfe die Auflösung des Simulators

## Lizenz

MIT - Nutze auf eigene Verantwortung!

## Support

Für Probleme: Issues erstellen oder PR einreichen 🚀