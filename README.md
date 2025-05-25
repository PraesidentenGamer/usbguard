# USBGuard

USBGuard ist ein kleines Python-Tool mit einer grafischen Benutzeroberfläche (GUI), das regelmäßig alle angeschlossenen USB-Geräte anzeigt und überwacht. Die Liste der USB-Geräte soll automatisch alle 5 Sekunden aktualisiert werden, allerdings funktioniert diese automatische Aktualisierung derzeit noch nicht zuverlässig.

---

## Features

- Übersichtliche GUI zur Anzeige aller erkannten USB-Geräte  
- (Geplant) Automatische Aktualisierung der Geräteanzeige alle 5 Sekunden (funktioniert nicht zuverlässig)  
- Zeigt Beschreibung und DeviceID der USB-Geräte an  
- Plattformübergreifend (getestet auf Windows)  
- Einfacher Start und Betrieb  

---

## Installation

1. Python 3.x installieren:  
   [Python Download](https://www.python.org/downloads/)

2. Abhängigkeiten installieren (falls nötig):  
   ```bash
   pip install tkinter 
   pip install ctypes
   pip install wmi
   pip instll time
   pip install os
   pip install threading
```

**Mitwirkende:**

CodeMajorX – Hauptentwickler und Maintainer

Beiträge und Verbesserungsvorschläge sind herzlich willkommen!

Hinweis: Das automatische Aktualisieren der USB-Geräteanzeige alle 5 Sekunden funktioniert aktuell nicht zuverlässig und wird noch verbessert.
Kontakt
Für Fragen oder Vorschläge öffne bitte ein Issue im Repository oder kontaktiere CodeMajorX.

© 2025 CodeMajorX

für meine Projekte nutze ich Python 3.12.9 in Windows 11 Pro


Englisch


# Usbguard

USBGUARD is a small python tool with a graphical user interface (GUI) that regularly shows and monitors all connected USB devices. The list of USB devices should be updated automatically every 5 seconds, but this automatic update is currently not working reliably.

---

## features

- Clear GUI for displaying all recognized USB devices  
- (planned) Automatic update of the device display every 5 seconds (does not work reliably)  
- Displays the description and deviceid of the USB devices  
- across platforms (tested for Windows)  
- easy start and operation  

---

## installation

1. Install python 3.x:  
   [Python Download] (https://www.python.org/downloads/)

2. Install dependencies (if necessary):  
  ```bash
   pip install tkinter 
   pip install ctypes
   pip install wmi
   pip instll time
   pip install os
   pip install threading
```

** Participant: **

Codemajorx - main developer and maintainer

Contributions and suggestions for improvement are welcome!

Note: The automatic update of the USB device display every 5 seconds does not currently work reliably and is still being improved.
contact
Please open an issue in the repository or contact Codemajorx for questions or suggestions.

© 2025 Codemajorx

For my projects I use Python 3.12.9 in Windows 11 Pro
