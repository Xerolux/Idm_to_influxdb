# Wolf CHA Modbus-Register

Detaillierte Dokumentation der Modbus-Register für Wolf CHA Wärmepumpen-Serie (CHA-16, CHA-20, CHA-Mono, CHA-Duo, CHA-Trio).

Letzte Aktualisierung: 31.01.2026

## Grundlagen

### Modbus-Konfiguration
- **Protokoll**: Modbus RTU oder TCP (mit Wolf Link Modul)
- **Baud Rate**: 9600 oder 19200
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Unit ID**: 1

### Kommunikation
- **Wolf Link**: Schnittstellenmodul für LAN/WLAN-Anbindung
- **Mod-Bus**: Integrierte Modbus-Schnittstelle
- **Gateway**: Erfordert oft zusätzliches Gateway-Modul

---

## Wichtige Register-Bereiche

### 1. Systemstatus (Adresse 0-99)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **Status** | 0 | Systemstatus | - | UInt16 | Hauptstatus der Wärmepumpe |
| **OperatingMode** | 1 | Betriebsart | - | UInt16 | 0=Standby, 1=Heizen, 2=Kühlen, 3=WW |
| **CompressorStage** | 2 | Verdichterstufe | - | UInt16 | 0=Aus, 1=Stufe 1, 2=Stufe 2 |
| **Alarm** | 3 | Alarm | - | UInt16 | 0=Kein Alarm, >0=Alarm vorhanden |
| **Warning** | 4 | Warnung | - | UInt16 | Warnungs-Flags |

### 2. Temperaturen (Adresse 100-299)

| Register | Adresse | Name | Einheit | Typ | Skalierung | Beschreibung |
|----------|---------|------|---------|-----|-----------|-------------|
| **OutdoorTemp** | 100 | Außentemperatur | °C | Int16 | 0.1 | Gemessene Außentemperatur |
| **SupplyTemp** | 101 | Vorlauftemperatur | °C | Int16 | 0.1 | Aktuelle Vorlauftemperatur |
| **ReturnTemp** | 102 | Rücklauftemperatur | °C | Int16 | 0.1 | Aktuelle Rücklauftemperatur |
| **DHWTempTop** | 103 | WW oben | °C | Int16 | 0.1 | Warmwasser oben |
| **DHWTempBottom** | 104 | WW unten | °C | Int16 | 0.1 | Warmwasser unten |
| **SourceTempIn** | 105 | Quellen-Eingang | °C | Int16 | 0.1 | Wärmequelle Eingang |
| **SourceTempOut** | 106 | Quellen-Ausgang | °C | Int16 | 0.1 | Wärmequelle Ausgang |
| **RoomTemp** | 107 | Raumtemperatur | °C | Int16 | 0.1 | Interne Raumtemperatur |

### 3. Leistung und Energie (Adresse 300-399)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **CurrentPower** | 300 | Aktuelle Leistung | kW | Float32 | Aktuelle elektrische Leistung |
| **ThermalPower** | 302 | Thermische Leistung | kW | Float32 | Aktuelle thermische Leistung |
| **EnergyHeating** | 304 | Wärme Heizen | kWh | Float32 | Gesamte Wärmemenge Heizen |
| **EnergyCooling** | 306 | Wärme Kühlen | kWh | Float32 | Gesamte Wärmemenge Kühlen |
| **EnergyDHW** | 308 | Wärme WW | kWh | Float32 | Gesamte Wärmemenge Warmwasser |
| **EnergyTotal** | 310 | Wärme gesamt | kWh | Float32 | Gesamt erzeugte Wärmemenge |

### 4. Sollwerte (schreibbar!) (Adresse 500-599)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **SetpointRoomTemp** | 500 | Raum-Soll | °C | Int16 | 15 | 25 | Raumtemperatur-Sollwert (schreibbar!) |
| **SetpointDHWTemp** | 501 | WW-Soll | °C | Int16 | 45 | 65 | Warmwasser-Sollwert (schreibbar!) |
| **SetpointSupplyTemp** | 502 | Vorlauf-Soll | °C | Int16 | 20 | 70 | Vorlauf-Sollwert (schreibbar!) |
| **CurveHeating** | 503 | Heizkurve | - | Float32 | 0.2 | 2.5 | Heizkurvensteigung (schreibbar!) |
| **CurveCooling** | 504 | Kühlkurve | - | Float32 | 0.2 | 2.5 | Kühlkurvensteigung (schreibbar!) |
| **CurveOffset** | 505 | Heizkurven-Offset | K | Float32 | -5 | +5 | Parallelverschiebung (schreibbar!) |

### 5. Pumpen und Ventile (Adresse 600-699)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **CircPumpStatus** | 600 | Umwälzpumpe | - | UInt16 | 0=Aus, 1=An |
| **CircPumpSpeed** | 601 | Pumpendrehzahl | % | UInt16 | Umwälzpumpen-Drehzahl |
| **SourcePumpStatus** | 602 | Quellenpumpe | - | UInt16 | Status der Quellenpumpe |
| **BrinePumpStatus** | 603 | Solepumpe | - | UInt16 | Status der Solepumpe |
| **ValveHeating** | 604 | Ventil Heizen | - | UInt16 | Ventilstatus Heizung |
| **ValveCooling** | 605 | Ventil Kühlen | - | UInt16 | Ventilstatus Kühlung |
| **ValveDHW** | 606 | Ventil WW | - | UInt16 | Ventilstatus Warmwasser |

### 6. Warmwasser (Adresse 700-799)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **DHWMode** | 700 | WW-Modus | - | UInt16 | ✅ | ✅ | 0=Auto, 1=Manuell (schreibbar!) |
| **DHWTemperature** | 701 | WW-Temperatur | °C | Int16 | ✅ | ❌ | Aktuelle WW-Temperatur |
| **DHWSetpoint** | 702 | WW-Soll | °C | Int16 | ✅ | ✅ | 45 | 65 | Sollwert (schreibbar!) |
| **DHWStatus** | 703 | WW-Status | - | UInt16 | ✅ | ❌ | 0=Bereit, 1=Laden |
| **DHWBoostTime** | 704 | Boost-Zeit | h | UInt16 | ✅ | ✅ | Startzeit (schreibbar!) |
| **DHWComfortMode** | 705 | Komfortmodus | - | UInt16 | ✅ | ✅ | 0=Eco, 1=Komfort (schreibbar!) |

### 7. Smart Grid / PV-Integration (Adresse 800-899)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **SGReadyStatus** | 800 | SG-Ready | - | UInt16 | ✅ | ❌ | Smart Grid Ready Status |
| **PowerLimit** | 801 | Leistungsbegrenzung | % | UInt16 | ✅ | ✅ | Maximalleistung (schreibbar!) |
| **PVPower** | 802 | PV-Leistung | kW | Float32 | ✅ | ❌ | Aktuelle PV-Leistung |
| **GridPower** | 803 | Netzleistung | kW | Float32 | ✅ | ❌ | Netzbezug/-einspeisung |
| **OperatingModeSG** | 804 | SG-Betrieb | - | UInt16 | ✅ | ✅ | Smart Grid Modus (schreibbar!) |

### 8. Fehler (Adresse 900-999)

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **ErrorCode** | 900 | Fehler-Code | UInt16 | Aktueller Fehler-Code |
| **ErrorText** | 901-910 | Fehlertext | String | Fehlerbeschreibung |
| **ResetError** | 999 | Fehler quittieren | UInt16 | Schreiben quittiert Fehler |

---

## Wichtige Hinweise

### Wolf CHA Modelle
- **CHA-16**: Monoblock 16 kW
- **CHA-20**: Monoblock 20 kW
- **CHA-Mono**: Einstufige Verdichter
- **CHA-Duo**: Zweistufige Verdichter
- **CHA-Trio**: Dreistufige Verdichter

### Wolf Link Modul
- Ermöglicht TCP/IP Anbindung
- Integriertes Web-Interface
- BMS-Schnittstelle

### Schreibbare Register
- ✅ **500-505**: Solltemperaturen, Heizkurven
- ✅ **700-705**: Warmwasser-Steuerung
- ✅ **801, 804**: Smart Grid-Steuerung

---

## Nützliche Links

- [Wolf Downloadcenter](https://www.wolf.eu/de-de/professional/downloads/downloadcenter)
- [Wolf Smartset](https://www.wolf-smartset.com/)
- [Wolf CHA Support Discussion](https://github.com/evcc-io/evcc/discussions/25457)
- [Wolf CHA Manual](https://www.heima24.de/shop/images/products/media/betr-wolf-cha-16-20.pdf)

---

**Version**: 1.0
**Letztes Update**: 31.01.2026
**Maintainer**: Xerolux
**Projekt**: [idm-metrics-collector](https://github.com/Xerolux/idm-metrics-collector)
