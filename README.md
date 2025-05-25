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
