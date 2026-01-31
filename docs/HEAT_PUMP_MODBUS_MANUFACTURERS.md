# Wärmepumpen-Hersteller mit Modbus-Unterstützung

Letzte Aktualisierung: 31.01.2026

## Übersicht

Diese Dokumentation listet Wärmepumpen-Hersteller auf, die Modbus-Schnittstellen zur Anbindung an Gebäudeautomation, Smart-Home-Systeme und Energiemanagement-Lösungen anbieten.

## Hersteller mit Modbus-Unterstützung

### ✅ Vollständig unterstützte Hersteller

#### 1. **IDM (Injection Development)**
- **Produkte**: Navigator 2.0, Kubrix, Aero
- **Modbus**: Modbus TCP, integrierte Luxtronik-Steuerung
- **Dokumentation**: Umfassende Register-Liste (siehe unten)
- **Besonderheiten**:
  - Sehr viele lesbare Register (1000+ Sensoren)
  - Schreibbare Register für Steuerung
  - Integrierte Smart-Grid-Funktionen
  - Multi-Zonen und Multi-Heizkreis-Unterstützung

#### 2. **Viessmann**
- **Produkte**: Vitocal 200-S, Vitocal 222-G, Vitocal 250-SH, Vitocal 300-G
- **Modbus**: Vitotronic 200 / Vitotronic 333 mit Modbus-TCP-Adapter
- **Dokumentation**:
  - [Vitocal 200-S Modbus](https://community.viessmann.de/t5/Waermepumpe-Hybridsysteme/Vitocal-200-S-Modbus-Schnittstelle-in-Steuerungeinbinden/td-p/522254)
  - [Modbus Interface](https://community.viessmann.de/t5/Waermepumpe-Hybridsysteme/Modbus-Interface/td-p/333200)
- **Besonderheiten**:
  - Außentemperatur, Vorlauftemperatur, Rücklauftemperatur
  - Energiezähler, Betriebsstunden
  - Statusmeldungen und Fehlercodes

#### 3. **Stiebel Eltron**
- **Produkte**: WPL A Serie, WPL 20A, WPL 12 Trend, WPL 25
- **Modbus**: ISG Web mit Modbus TCP/IP-Schnittstelle
- **Dokumentation**: [Stiebel Eltron Modbus](https://www.stiebel-eltron.ch/de/home/produkte-loesungen/erneuerbare_energien/regelung_energiemanagement/modbus.html)
- **Besonderheiten**:
  - ISG (Internet Service Gateway) für Fernzugriff
  - Umfangreiche Energie- und Tempraturwerte
  - Integrierte Fehlerdiagnose
  - Schlafmodus, Party-Modus steuerbar

#### 4. **Wolf Heiztechnik**
- **Produkte**: CHA Mono, CHA Duo, CHA Trio
- **Modbus**: Wolf Link Modul (Schnittstellenmodul für LAN/WLAN)
- **Dokumentation**: [Wolf Downloadcenter](https://www.wolf.eu/de-de/professional/downloads/downloadcenter)
- **Besonderheiten**:
  - Mod-Bus-Schnittstellen-Set extern verfügbar
  - Temperaturwerte, Energiewerte
  - Betriebszustände und Fehlermeldungen
  - Zeitprogramme steuerbar

#### 5. **NIBE**
- **Produkte**: S-Serie (S1245, S1255, S2125, S2145, S2255, S3125, S3155, S3255, S3455)
- **Modbus**: SMO S40 Steuermodul mit Modbus RTU/TCP
- **Dokumentation**: [MODBUS S-SERIES](https://nibe.ua/document_search/file?test=/files/3/documents/MODBUS%20S%20%D1%81%D0%B5%D1%80%D0%B8%D1%8F%20(en).pdf)
- **Besonderheiten**:
  - Exhaustmesser, Außentemperatur
  - Verdichterstatus, Heizkurvenparameter
  - Warmwasserbereitung
  - PV-Überschuss-Steuerung (EME20 Modul)

#### 6. **Mitsubishi Electric**
- **Produkte**: Ecodan Serie (PUHZ, SUZ, EERQ)
- **Modbus**: MELCloud-to-Modbus RTU Adapter (z.B. IN485MIT001A000)
- **Dokumentation**: [Mitsubishi Ecodan zu Modbus](https://www.hms-networks.com/p/in485mit001a000-mbs-mit-mitsubishi-electric-ecodan-air-to-water-heat-pumps-to-modbus-rtu)
- **Besonderheiten**:
  - Leistungsabgabe, Temperaturwerte
  - Smart-Meter-Integration
  - Fehlerstatus
  - Betriebsarten-Steuerung

#### 7. **Vaillant**
- **Produkte**: aroTHERM, flexoTHERM, geoTHERM Serie
- **Modbus**: Smart Connect Modbus Gateway
- **Dokumentation**: [Vaillant Smart Connect](https://www.ise.de/produkte/smart-connect-serie/modbus-vaillant)
- **Besonderheiten**:
  - multiMATIC Steuerung
  - Energieverbrauchswerte
  - Temperaturen und Drücke
  - Fehlerdiagnose

### 📊 Hersteller mit eingeschränkter Modbus-Unterstützung

#### 8. **Bosch**
- **Produkte**: Compress 6000, 7000, 8000 AW, GWW
- **Modbus**: teilweise über Controller-Erweiterungen
- **Bemerkung**: Nicht alle Modelle haben nativen Modbus, oft Zusatzhardware nötig

#### 9. **Buderus**
- **Produkte**: Logatherm Serie
- **Modbus**: Über Logamatic TC100 mit Modbus-Modul
- **Bemerkung**: Abhängig vom verwendeten Regler

#### 10. **Ochsner**
- **Produkte**: GMLW, GMSW Serie
- **Modbus**: OWD Regler mit optionaler Modbus-Schnittstelle
- **Bemerkung**: OWD necessary, nicht immer serienmäßig

#### 11. **Alpha Innotec**
- **Produkte**: Alpha-Innotec Serie (gehört zu Stiebel Eltron)
- **Modbus**: Luxtronik-Steuerung mit Modbus TCP/IP
- **Dokumentation**: [Luxtronik Control](https://www.alpha-innotec.com/en/products/accessories/control/luxtronik)
- **Besonderheiten**: Gleiche Basis wie Stiebel Eltron, sehr ähnliche Register

#### 12. **Campini**
- **Produkte**: Aquarea Serie
- **Modbus**: Panasonic Aquarea Smart Cloud Modbus
- **Bemerkung**: Meist Cloud-basierte Lösung, nativer Modbus selten

#### 13. **Techneco**
- **Produkte**: Aquabella Serie
- **Modbus**: TeCalor/Techneco Regler mit Modbus (siehe Stiebel Eltron)
- **Dokumentation**: [TeCalor Modbus](https://www.tecalor.de/content/dam/tec/de/downloads/Modbus_Bedienungsanleitung.pdf)
- **Besonderheiten**: Verwendet ISG-Technologie

#### 14. **ATAG**
- **Produkte**: i, W, KE Serie
- **Modbus**: OneControl Gateway mit Modbus-Option
- **Bemerkung**: Nicht alle Modelle, depends on Version

#### 15. **Daikin**
- **Produkte**: Altherma Serie
- **Modbus**: Optional über BRP069A61 Modbus-Adapter
- **Bemerkung**: Meist optional, nicht serienmäßig

#### 16. **Worcester Bosch**
- **Produkte**: Greenstar Serie
- **Modbus**: Über Bosch EasyControl + Adapter
- **Bemerkung**: Indirekte Lösung, kein nativer Modbus

## Vergleichstabelle der wichtigsten Hersteller

| Hersteller | Modbus Typ | Native Unterstützung | Register-Umfang | Schreibbar | Empfehlung |
|------------|------------|---------------------|-----------------|------------|-------------|
| **IDM** | TCP | ✅ Ja | 1000+ | ✅ Ja | ⭐⭐⭐⭐⭐ Beste Unterstützung |
| **Viessmann** | TCP | ✅ Ja | 200+ | ✅ Ja | ⭐⭐⭐⭐⭐ Sehr gut |
| **Stiebel Eltron** | TCP | ✅ Ja | 150+ | ✅ Ja | ⭐⭐⭐⭐⭐ Sehr gut |
| **Wolf** | TCP | ✅ Ja | 100+ | ✅ Ja | ⭐⭐⭐⭐ Gut |
| **NIBE** | RTU/TCP | ✅ Ja | 150+ | ✅ Ja | ⭐⭐⭐⭐ Gut |
| **Mitsubishi** | RTU | ✅ Ja | 100+ | ⚠️ Eingeschränkt | ⭐⭐⭐ Mittel |
| **Vaillant** | TCP | ✅ Ja | 100+ | ✅ Ja | ⭐⭐⭐⭐ Gut |
| **Alpha Innotec** | TCP | ✅ Ja | 150+ | ✅ Ja | ⭐⭐⭐⭐ Gut (ähnlich Stiebel) |
| **Bosch/Buderus** | RTU | ⚠️ Optional | 50+ | ⚠️ Eingeschränkt | ⭐⭐⭐ Mittel |
| **Ochsner** | TCP | ⚠️ Optional | 80+ | ⚠️ Eingeschränkt | ⭐⭐⭐ Mittel |
| **Daikin** | RTU | ⚠️ Adapter | 60+ | ⚠️ Eingeschränkt | ⭐⭐ Mittel |
| **Panasonic** | TCP | ⚠️ Cloud | 80+ | ❌ Nein | ⭐⭐ Cloud-basiert |

## Typische Modbus-Register (Allgemein)

Die meisten Hersteller bieten ähnliche Basis-Register an:

### Temperaturwerte (typisch Adressen 1000-1100)
- Außentemperatur
- Vorlauftemperatur
- Rücklauftemperatur
- Warmwasser-Temperaturen (Speicher oben/unten)
- Quellentemperaturen (Luft, Sole, Erdreich)

### Energiezähler (typisch Adressen 1700-1800)
- Wärmemenge gesamt (kWh)
- Wärmemenge Heizen
- Wärmemenge Warmwasser
- Elektrische Arbeit (kWh)
- Betriebsstunden

### Status-Register (typisch Adressen 2000-2100)
- Systemstatus
- Verdichterstatus
- Pumpenstatus
- Ventilstellungen
- Fehlercodes

### Steuer-Register (bei unterstützten Herstellern)
- Solltemperatur setzen
- Betriebsart wechseln
- Zeitprogramme
- Smart-Grid-Parameter

## Empfehlung für neue Installationen

### Für maximale Steuerungsmöglichkeiten:
1. **IDM Navigator** - Beste Unterstützung, alle Register lesbar und schreibbar
2. **Viessmann Vitocal** - Sehr gute Dokumentation, breite Unterstützung
3. **Stiebel Eltron / Alpha Innotec** - Gute ISG-Integration

### Für PV-Integration und Smart-Home:
1. **IDM** - Native Smart-Grid-Funktionen, PV-Überschuss-Steuerung
2. **NIBE** - Gute PV-Integration mit EME20 Modul
3. **Wolf** - Smart-Grid-Ready Modelle

### Für Cloud-freie lokale Automation:
1. **IDM** - Vollständig lokal steuerbar
2. **Stiebel Eltron** - ISG ermöglicht lokalen Zugriff
3. **Viessmann** - Vitotronic mit Modbus-TCP

## Hinweise zur Integration

### Adressierung
- **IDM**: Holding Registers, meist Adressen 74-2000+
- **Viessmann**: Holding/Floating Registers, Adressen je nach Regler
- **Stiebel Eltron**: ISG Web, meist Adressen 1000-5000
- **Wolf**: Mod-Bus, Adressen 0-1000 typisch

### Datentypen
- Temperaturen meist Float32 (IEEE 754)
- Energiewerte meist UInt32 oder Float32
- Status-Register meist UInt16 oder Enum
- Leistungswerte meist Float32

### Byte-Order
- Meist Big-Endian Byte Order
- Word Order variiert (Big-Endian oder Little-Endian)
- IDM: Big-Endian Byte, Little-Endian Word

## Nützliche Links

- [Wikiversity: Heat Pump Modbus](https://en.wikiversity.org/wiki/Heat_pump_and_Modbus)
- [AKKU-Doktor: Wärmepumpen-Schnittstellen](https://akkudoktor.net/t/warmepumpen-mit-ansteuerbaren-schnittstellen-0-10v-modbus-fur-heizungsregelung-technische-alternative/9463)
- [haustechnikdialog: Wärmepumpen-Forum](https://www.haustechnikdialog.de/Forum/t/242894/Welche-Waermepumpe-fuer-offene-Schnittstellen-Hausautomatisierung-)

## Beiträge

Wenn Sie Informationen zu anderen Herstellern haben oder Register-Dokumentationen beisteuern möchten, erstellen Sie bitte ein Pull-Request oder Issue im GitHub Repository.

---

**Dokumentation Version**: 1.0
**Letztes Update**: 31.01.2026
**Maintainer**: Xerolux
**Projekt**: [idm-metrics-collector](https://github.com/Xerolux/idm-metrics-collector)
