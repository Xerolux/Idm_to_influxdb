# IDM Metrics Collector

[![GitHub Release][releases-shield]][releases]
[![Downloads][downloads-shield]][releases]
[![License][license-shield]](LICENSE)
[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

> **Die professionelle Monitoring-Lösung für IDM Wärmepumpen (Navigator 2.0)**
>
> Echtzeit-Überwachung, Langzeitanalyse, KI-Anomalieerkennung und vollständige Steuerung - alles in einer Docker-basierten All-in-One Lösung.

![Demo](docs/images/demo.gif)

<details>
<summary>Screenshots (Klicken zum Ausklappen)</summary>
<br>

| Übersicht | Steuerung |
|:---:|:---:|
| ![Hauptseite](docs/images/screenshots/Hauptseite.png) | ![Steuerung](docs/images/screenshots/Steuerung.png) |

| Zeitplan | Protokolle |
|:---:|:---:|
| ![Zeitplan](docs/images/screenshots/Zeitplan.png) | ![Protokoll](docs/images/screenshots/Protokoll.png) |

| Benachrichtigung | Alarm |
|:---:|:---:|
| ![Benachrichtigung](docs/images/screenshots/Benachrichtigung.png) | ![Alarm](docs/images/screenshots/Alarm_Message.png) |

| KI Anomalie | Einstellung |
|:---:|:---:|
| ![KI_Anomalie](docs/images/screenshots/KI_Anomalie.png) | ![Einstellung](docs/images/screenshots/Einstellung.png) |

| MQTT | Wartung |
|:---:|:---:|
| ![MQTT](docs/images/screenshots/MQTT.png) | ![Wartung](docs/images/screenshots/Wartung.png) |

| Tools | Login |
|:---:|:---:|
| ![Codegenerator](docs/images/screenshots/Codegenerator.png) | ![Login](docs/images/screenshots/Login.png) |

</details>

---

## Warum IDM Metrics Collector?

Der IDM Metrics Collector bietet ein leistungsstarkes, eigenständiges Dashboard - einfacher, schneller und perfekt integriert für IDM Wärmepumpen.

### Highlights

- Modernes Dashboard mit Drag & Drop, Zoom & Dark Mode
- Dual Y-Achsen für Temperatur + Leistung in einem Chart
- Stat & Gauge Panels für Soll/Ist Vergleiche
- Chart Templates - One-Click Dashboards für alle Anwendungsfälle
- KI-Anomalie-Erkennung warnt bei abnormalem Verhalten
- Stabile Modbus-Verbindung mit automatischer Wiederverbindung
- Dark Mode mit System-Preference-Unterstützung

---

## Dokumentation

- [Handbuch (PDF)][docs-pdf] - Ausführliche Bedienungsanleitung
- [Online Dokumentation][docs-online] - Vollständige Feature-Referenz

---

## Schnellstart

### Voraussetzungen

- Docker & Docker Compose
- Netzwerkverbindung zur IDM Wärmepumpe (Navigator 2.0)

### Installation & Start

```bash
# Repository klonen
git clone https://github.com/Xerolux/idm-metrics-collector.git
cd idm-metrics-collector

# Starten
docker compose up -d

# Im Browser öffnen
# http://<deine-ip>:5008
```

### Ersteinrichtung

1. **IP der Wärmepumpe** eingeben
2. **Sicheres Passwort** vergeben (min. 6 Zeichen)
3. **Fertig!** Das Dashboard ist sofort live

---

## Funktionen

### Dashboard

Das Herzstück der Anwendung - alles auf einen Blick.

**Kernfunktionen:**
- **Live-Daten**: Außentemperatur, Vorlauf, Rücklauf, Speicher, Warmwasser
- **Drag & Drop**: Widgets beliebig anordnen
- **Zoom & Pan**: Mausrad oder Drag zum Zoomen, Ctrl+Drag zum Verschieben
- **Dual Y-Achsen**: Temperatur (links) + Leistung (rechts) in einem Chart
- **Vollbildmodus**: Jeder Chart im Fullscreen
- **Dark Mode**: Automatisch oder manuell umschaltbar

**Panel-Typen:**
- **Line Charts**: Zeitverläufe mit beliebig vielen Serien
- **Stat Panels**: Einzelwerte als große Zahlen mit Trend-Anzeige
- **Gauge Panels**: Tachometer für COP, Effizienz, etc.

**Templates:**
- Temperaturübersicht
- Leistungsanalyse
- Effizienz-Monitor
- Heizkreis Detail
- Warmwasser-Monitor
- Solar-Integration

### Steuerung

Volle Kontrolle über deine Wärmepumpe.

- **Betriebsmodi**: Heizen, Kühlen, Auto, Eco
- **Temperaturen**: Sollwerte für Heizkreise und Warmwasser
- **Sofort-Aktionen**: Einmalige Warmwasserladung per Klick
- **EEPROM-Schutz**: Warnung bei zyklischen Schreibzugriffen

### Zeitpläne

Intelligente Automatisierung für Komfort und Effizienz.

- **Wochenpläne**: Individuelle Pläne für jeden Wochentag
- **Drag & Drop**: Intuitive Bedienung
- **Mehrfach-Trigger**: Verschiedene Aktionen zu verschiedenen Zeiten

### Benachrichtigungen & KI

Das System wacht über deine Anlage - 24/7.

**Alert-Typen:**
- **Schwellwert-Alerts**: Temperatur/Druck überschritten
- **Status-Alerts**: Verdichter aus, Fehlermeldung, etc.
- **KI-Anomalien**: Maschinelles Lernen erkennt abnormales Verhalten

**Kanäle:**
- Push (ntfy), MQTT, Telegram, Signal, Discord, E-Mail, WebDAV

### Konfiguration

Alles an einem Ort.

- **Verbindung**: Modbus-Parameter mit automatischer Wiederverbindung
- **Heizkreise**: A, B, C aktivieren
- **MQTT**: Home Assistant Integration
- **Benachrichtigungen**: Alle Kanäle konfigurieren
- **Backup**: Automatische Backups mit WebDAV-Upload
- **Netzwerk**: IP-Whitelist/Blacklist
- **Updates**: Automatisch via Watchtower

### Logs

Behalte den Überblick.

- **Echtzeit-Logs**: Alle Systemereignisse live
- **Filterbare Ansicht**: Modbus, Scheduler, Web, Alerts
- **Farbcodierung**: Info, Warning, Error

### Tools & Service

Für Profis und Technik-Fans.

- **Techniker-Codes**: Temporäre Fachmann-Codes generieren
- **System-Check**: Gesundheit aller Dienste

---

## Technische Details

### Stack

**Backend:**
- Python 3.11+
- Flask + Waitress (Production Server)
- Modbus TCP (pymodbus) mit Exponential Backoff
- VictoriaMetrics (Time Series Database)
- River (Online Machine Learning)

**Frontend:**
- Vue 3 + Composition API
- PrimeVue (UI Components)
- Chart.js + vue-chartjs
- Tailwind CSS 4

**Docker:**
- Multi-stage build
- Alpine-based images
- Automatic restart policies
- Watchtower für automatische Updates

### Verbindungsstabilität

Die Modbus- und AI-Service-Verbindungen wurden für maximale Stabilität optimiert:

- **Exponential Backoff**: Automatische Wiederverbindung mit steigender Verzögerung
- **Health Monitoring**: Verbindungsstatistiken und Fehlertracking
- **Graceful Degradation**: System bleibt funktionsfähig auch bei temporären Ausfällen
- **Retry-Logik**: Automatische Wiederholung bei transienten Fehlern

### Performance

- **Polling**: 60 Sekunden (konfigurierbar)
- **Data Points**: Intelligentes Downsampling
- **Caching**: API-Responses gecacht
- **Bundle Size**: ~500KB gzipped

### Sicherheit

- **Passwort**: Min. 6 Zeichen, gehashed
- **Session**: HTTPOnly, SameSite=Lax
- **Rate Limiting**: 200 req/min
- **Security Headers**: CSP, X-Frame-Options, etc.
- **Network Security**: IP-Whitelist/Blacklist

---

## Support & Community

**Fragen? Probleme? Ideen?**

- [Issue erstellen][issues]
- [Discord Community][discord]
- [Dokumentation][docs-online]

---

## Lizenz

MIT License - siehe [LICENSE](LICENSE)

---

## Danksagung

An alle Contributer, Tester und Community-Mitglieder, die dieses Projekt möglich machen!

Besonderer Dank an:
- IDM für die offene Modbus-Spezifikation
- Die Home-Assistant-Community
- Alle Beta-Tester

---

**Viel Spaß mit deinem IDM Metrics Collector!**

<!-- Badge Links -->
[releases-shield]: https://img.shields.io/github/release/xerolux/idm-metrics-collector.svg?style=for-the-badge
[releases]: https://github.com/xerolux/idm-metrics-collector/releases
[downloads-shield]: https://img.shields.io/github/downloads/xerolux/idm-metrics-collector/latest/total.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/xerolux/idm-metrics-collector.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[docs-pdf]: docs/IDM_Metrics_Collector_Handbuch.pdf
[docs-online]: docs/MANUAL.md
[issues]: https://github.com/xerolux/idm-metrics-collector/issues
