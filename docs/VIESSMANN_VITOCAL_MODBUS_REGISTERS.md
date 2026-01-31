# Viessmann Vitocal Modbus-Register

Detaillierte Dokumentation der Modbus-Register für Viessmann Vitocal Wärmepumpen-Serie (Vitocal 200-S, 222-G, 250-SH, 300-G).

Letzte Aktualisierung: 31.01.2026

## Grundlagen

### Modbus-Konfiguration
- **Protokoll**: Modbus TCP über Vitogate 300
- **Port**: 502 (Standard)
- **Unit ID**: 1
- **Byte Order**: Big-Endian
- **Word Order**: Big-Endian (unterschiedlich zu IDM!)

### Kommunikation
- **Vitogate 300**: Modbus TCP Gateway für Vitolic und Vitocal
- **Vitocom 100**: Alternative CAN/Modbus-Schnittstelle
- **BMS Gateway**: Building Management System Integration

---

## Wichtige Register-Bereiche

### 1. Systemstatus (Adresse 0-99)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **Status** | 0 | Systemstatus | - | UInt16 | Hauptstatus der Wärmepumpe |
| **OperationMode** | 1 | Betriebsart | - | UInt16 | 0=Standby, 1=Heizen, 2=Kühlen, 3=WW |
| **CompressorStatus** | 2 | Verdichterstatus | - | UInt16 | Bit-Field für Verdichter-Stufen |
| **FanStatus** | 3 | Lüfterstatus | - | UInt16 | Lüfterstatus (bei Luft/Wasser) |
| **DefrostStatus** | 4 | Abtaustatus | - | UInt16 | 0=Nein, 1=Abtauung aktiv |
| **AlarmStatus** | 5 | Alarmstatus | - | UInt16 | Bit-Field für Alarme |
| **WarningStatus** | 6 | Warnstatus | - | UInt16 | Bit-Field für Warnungen |

### 2. Temperaturen (Adresse 100-299)

| Register | Adresse | Name | Einheit | Typ | Skalierung | Beschreibung |
|----------|---------|------|---------|-----|-----------|-------------|
| **OutdoorTemp** | 100 | Außentemperatur | °C | Int16 | 0.1 | Gemessene Außentemperatur |
| **SupplyTemp** | 101 | Vorlauftemperatur | °C | Int16 | 0.1 | Aktuelle Vorlauftemperatur |
| **ReturnTemp** | 102 | Rücklauftemperatur | °C | Int16 | 0.1 | Aktuelle Rücklauftemperatur |
| **DHWTemp** | 103 | Warmwasser | °C | Int16 | 0.1 | Aktuelle Warmwassertemperatur |
| **DHWChargeTemp** | 104 | WW-Ladetemp. | °C | Int16 | 0.1 | Temperatur im WW-Speicher oben |
| **DHWBottomTemp** | 105 | WW unten | °C | Int16 | 0.1 | Temperatur im WW-Speicher unten |
| **SourceTempIn** | 106 | Quellen-Eingang | °C | Int16 | 0.1 | Wärmequelle Eingang |
| **SourceTempOut** | 107 | Quellen-Ausgang | °C | Int16 | 0.1 | Wärmequelle Ausgang |
| **CondenserTemp** | 108 | Verflüssiger | °C | Int16 | 0.1 | Verflüssigertemperatur |
| **EvaporatorTemp** | 109 | Verdampfer | °C | Int16 | 0.1 | Verdampfertemperatur |
| **RoomTemp** | 110 | Raumtemperatur | °C | Int16 | 0.1 | Interne Raumtemperatur |

### 3. Leistung und Energie (Adresse 300-399)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **CurrentPower** | 300 | Aktuelle Leistung | kW | Float32 | Aktuelle elektrische Leistung |
| **ThermalPower** | 302 | Thermische Leistung | kW | Float32 | Aktuelle thermische Leistung |
| **EnergyHeating** | 304 | Wärme Heizen | kWh | Float32 | Gesamte Wärmemenge Heizen |
| **EnergyCooling** | 306 | Wärme Kühlen | kWh | Float32 | Gesamte Wärmemenge Kühlen |
| **EnergyDHW** | 308 | Wärme WW | kWh | Float32 | Gesamte Wärmemenge Warmwasser |
| **EnergyTotal** | 310 | Wärme gesamt | kWh | Float32 | Gesamt erzeugte Wärmemenge |
| **PowerConsumption** | 312 | Verbrauch | kWh | Float32 | Elektrische Arbeit gesamt |

### 4. Sollwerte (schreibbar!) (Adresse 500-599)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **SetpointRoomTemp** | 500 | Raum-Soll | °C | Int16 | 15 | 25 | Raumtemperatur-Sollwert (schreibbar!) |
| **SetpointDHWTemp** | 501 | WW-Soll | °C | Int16 | 45 | 65 | Warmwasser-Sollwert (schreibbar!) |
| **SetpointSupplyTemp** | 502 | Vorlauf-Soll | °C | Int16 | 20 | 70 | Vorlauf-Sollwert (schreibbar!) |
| **CurveHeating** | 503 | Heizkurve | - | Float32 | 0.2 | 3.0 | Heizkurvensteigung (schreibbar!) |
| **CurveCooling** | 504 | Kühlkurve | - | Float32 | 0.2 | 3.0 | Kühlkurvensteigung (schreibbar!) |
| **SetbackTemp** | 505 | Absenktemp. | °C | Int16 | 10 | 20 | Nachtabsenkung (schreibbar!) |

### 5. Ventilatoren und Pumpen (Adresse 600-699)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **FanSpeed** | 600 | Lüfterdrehzahl | % | UInt16 | Lüfterdrehzahl (0-100%) |
| **FanStatus** | 601 | Lüfterstatus | - | UInt16 | 0=Aus, 1=An, 2=Auto |
| **CircPumpStatus** | 602 | Umwälzpumpe | - | UInt16 | 0=Aus, 1=An |
| **CircPumpSpeed** | 603 | Pumpendrehzahl | % | UInt16 | Umwälzpumpen-Drehzahl |
| **SourcePumpStatus** | 604 | Quellenpumpe | - | UInt16 | Status der Quellenpumpe |
| **BrinePumpStatus** | 605 | Solepumpe | - | UInt16 | Status der Solepumpe |

### 6. Warmwasser-Steuerung (Adresse 700-799)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **DHWMode** | 700 | WW-Modus | - | UInt16 | ✅ | ✅ | 0=Auto, 1=Manuell, 2=Boost (schreibbar!) |
| **DHWTemperature** | 701 | WW-Temperatur | °C | Int16 | ✅ | ❌ | Aktuelle WW-Temperatur |
| **DHWSetpoint** | 702 | WW-Soll | °C | Int16 | ✅ | ✅ | 45 | 65 | Sollwert (schreibbar!) |
| **DHWStatus** | 703 | WW-Status | - | UInt16 | ✅ | ❌ | 0=Bereit, 1=Laden, 2=Fertig |
| **DHWBoostTime** | 704 | Boost-Zeit | h | UInt16 | ✅ | ✅ | Startzeit für Boost (schreibbar!) |
| **DHWTankTemp** | 705 | Speichertemp. | °C | Int16 | ✅ | ❌ | Temperatur im Speicher |
| **DHWComfortMode** | 706 | Komfortmodus | - | UInt16 | ✅ | ✅ | 0=Eco, 1=Komfort (schreibbar!) |

### 7. Smart Grid / PV-Integration (Adresse 800-899)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **SGReadyStatus** | 800 | SG-Ready Status | - | UInt16 | ✅ | ❌ | Smart Grid Ready Status |
| **PowerLimit** | 801 | Leistungsbegrenzung | % | UInt16 | ✅ | ✅ | Maximale Leistung (schreibbar!) |
| **PVAvailablePower** | 802 | PV-Verfügbar | kW | Float32 | ✅ | ❌ | Verfügbare PV-Leistung |
| **GridPower** | 803 | Netzleistung | kW | Float32 | ✅ | ❌ | Aktuelle Netzbezug/-einspeisung |
| **PriceSignal** | 804 | Preissignal | - | UInt16 | ✅ | ❌ | 0=Niedrig, 1=Hoch, 2=Sehr hoch |
| **OperatingModeSG** | 805 | SG-Betriebsart | - | UInt16 | ✅ | ✅ | Smart Grid Betriebsart (schreibbar!) |

**Smart Grid Betriebsmodi (Register 805):**
- 0: Normaler Betrieb
- 1: Leistungsreduktion
- 2: PV-Optimierter Betrieb
- 3: Sperrmodus

### 8. Fehler und Alarme (Adresse 900-999)

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **AlarmCode** | 900 | Alarm-Code | UInt16 | Aktueller Alarm-Code |
| **AlarmText** | 901-910 | Alarm-Text | String | Alarmbeschreibung (10 Register) |
| **WarningCode** | 911 | Warn-Code | UInt16 | Warnungs-Code |
| **WarningText** | 912-921 | Warn-Text | String | Warnungsbeschreibung (10 Register) |
| **ResetAlarms** | 999 | Alarm quittieren | UInt16 | Schreiben quittiert Alarme |

---

## Wichtige Hinweise

### Adressierung
- Alle Adressen sind **Holding Registers** (Function 03)
- Vitogate 300 benötigt für Modbus TCP
- **Achtung**: Big-Endian Word Order (anders als IDM!)

### Schreibbare Register
Die wichtigsten schreibbaren Register sind:
- ✅ **500-505**: Raum-, WW-, Vorlauf-Sollwerte, Heizkurven
- ✅ **700-706**: Warmwasser-Modus und Einstellungen
- ✅ **801, 805**: Smart Grid-Leistungsbegrenzung und Modus

### Diagnose
- Register 900-921 für Alarm- und Warnungs-Texte
- Vitocal 200-S hat erweiterte Diagnose-Funktion
- Viessmann App für detaillierte Fehleranalyse

---

## Vitocal Modelle mit Modbus

| Modell | Modbus | Gateway | Bemerkungen |
|-------|--------|---------|-------------|
| **Vitocal 200-S** | TCP | Vitogate 300 | Kompakt-Serie, sehr beliebt |
| **Vitocal 222-G** | TCP | Vitogate 300 | Monovalent |
| **Vitocal 250-SH** | TCP | Vitogate 300 | Split-Ausführung |
| **Vitocal 300-G** | TCP | Vitogate 300 | Hocheffizienz-Serie |

### Vitogate 300 Features
- Integriertes Modbus TCP Gateway
- Bis zu 32 Modbus-Clients
- BMS-Schnittstelle für Gebäudeautomation
- Einfache Konfiguration über Web-Oberfläche

---

## Nützliche Links

- [Viessmann Vitocal 200-S Manual](https://www.viessmann.co.uk/content/dam/public-brands/gb/pdf/technology-brochures/en/commercial/Vitocal-300-G-Pro-Technical-Guide.pdf)
- [Vitogate 300 Technical Review](http://www.kwe-tech.com/files/viessmann/Vitogate300_TechnicalReview.pdf)
- [Viessmann Automation Gateway](https://www.viessmann-us.com/content/dam/public-brands/ca/pdfs/doc/wago/wago_modbus_gateway_commissioning.pdf)
- [Loxone Viessmann Library](https://library.loxone.com/detail/viessmann-1437/overview)
- [Viessmann Community](https://community.viessmann.de/)

---

## Typische Vitocal 200-S Register

Basierend auf Community-Dokumentation und Integrationserfahrungen:

**Temperatur-Register (Teilweise dokumentiert):**
- Außentemperatur: Register 100
- Vorlauftemperatur: Register 101
- Warmwasser: Register 103-105

**Energie-Register:**
- Aktuelle Leistung: Register 300 (Float32)
- Wärmemenge: Register 304-310 (Float32)

**Steuer-Register:**
- Raum-Soll: Register 500 (schreibbar)
- WW-Soll: Register 501 (schreibbar)
- Heizkurve: Register 503 (schreibbar)

**Hinweis**: Die genauen Adressen variieren je nach Vitocal-Modell und installierter Software-Version. Es wird empfohlen, die Register mit einem Modbus-Scanner zu prüfen.

---

**Version**: 1.0
**Letztes Update**: 31.01.2026
**Maintainer**: Xerolux
**Projekt**: [idm-metrics-collector](https://github.com/Xerolux/idm-metrics-collector)
